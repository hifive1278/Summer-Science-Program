# Here for reference, I did not code this

import os, math
from astroquery.jplhorizons import Horizons

class ObserveRequest() :
    # Executed with start
    def __init__(self) :
        # Ask which mode to use 
        mod = input('\nSelect Mod [info, ephemeris, all, to text] : ')
        
        # Start the requested mod
        if mod == 'info' :
            self.info()
        elif mod == 'ephemeris':
            self.ephemeris()
        elif mod == 'all' :
            self.ephemeris(show_both = True)
        elif mod == 'to text' :
            self.to_text()

    # Collects crucial data from user
    def get_data(self, is_step = False) :
        self.name = input('\nTarget Asteroid : ')                             # Name of Asteroid
        self.mpc = input('MPC Code : ')                                       # MPC Code of Observatory
        self.telescope = input('Telescope : ')                                # Telescope Name 
        self.fov = input('Camera FOV [A x B] : ')                             # Camera FOV
        self.start = input('Start Date [YYYY-MM-DD] : ')                      # Start Point of Data
        self.stop = input('Stop Date [YYYY-MM-DD] : ')                        # End Point of Data
        if is_step :
            self.step = input('Step Size : ')                                 # Step Size
        print('')


    # Info - Prints information of telescope and asteroid
    def info(self, show_results = True, show_both = False) :
        # Load crucial data
        if show_results and not show_both :
            # For Info, we do not need step size
            self.get_data()
        else :
            # For Ephemerides, we need step size
            self.get_data(is_step = True)

        # Retrieve asteroid data from Horizons 
        obj = Horizons(id = self.name, location = self.mpc,
                       epochs = {'start': self.start, 'stop': self.stop,
                                 'step': '1m'})
        
        # Retrieve Sun's altitude data from Horizons
        sun = Horizons(id = '10', id_type = 'id', location = self.mpc,
                       epochs = {'start': self.start, 'stop': self.stop,
                                 'step': '1m'}).ephemerides()['EL']

        # Get Values : Date & Time, Alt, RA, DEC, T-O-M Angle, Moon Illumination, RA_rate, DEC_rate
        eph = obj.ephemerides()['datetime_str', 'EL', 'RA', 'DEC', 'lunar_elong', 'lunar_illum', 'V', 'RA_rate', 'DEC_rate']
        # Use Values : Date & Altitude Only
        part_eph = eph['datetime_str', 'EL']
        # Target Values : Transit Time, 30 Deg Rise, 30 Deg Set
        transit, rise30, set30, order = (None, None, None, -90.1)
        # Target Values : Evening Nautical Twilight, Morning Nautical Twilight
        evening_nt, morning_nt = (None, None)

        # Loop for Each Row of Table
        for i in range(1, len(part_eph)) :
            # Date & Time, Altitude of 1 min before
            DT_prev, EL_prev = tuple(part_eph[i-1])
            # Date & Time, Altitude of now
            DT_now, EL_now = tuple(part_eph[i])
            
            # Assign the time with the highest altitude as Transit Time
            transit, order = (DT_now, EL_now) if EL_now > order else (transit, order)
            # If Altitude exceeds 30 Deg for first time, rise30 = DT_now
            rise30 = DT_now if (int(EL_now) == 30 and int(EL_prev) < 30) else rise30
            # If Altitude falls down to 29 Deg for first time, set30 = DT_prev
            set30 =  DT_prev if (int(EL_now) == 29 and int(EL_prev) > 29) else set30
            # If Sun's Altitude exceeds 6 Deg, evening_nt = DT_prev
            evening_nt = DT_now if int(sun[i]) == -12 and int(sun[i-1]) > -12 else evening_nt
            # If Sun's Altitude falls down to 7 Deg, morning_nt = 
            morning_nt = DT_prev if int(sun[i]) == -11 and int(sun[i-1]) < -11 else morning_nt

        # Start & End of Observable Window
        ow_start = rise30 if rise30 > evening_nt else evening_nt
        ow_end = set30 if set30 <  morning_nt else morning_nt

        # Get the Observable Time
        self.make_time = lambda x: x.split(' ')[1].split(':')
        minute_len = lambda x: int(self.make_time(x)[0]) * 60 + int(self.make_time(x)[1])
        ow_len = minute_len(ow_end) - minute_len(ow_start)
        ow_len_str = '%02d:%02d' % (ow_len // 60, ow_len % 60)

        # Find the middle of observable window
        ow_mid = int(ow_len/2) + 1 if ow_len % 2 != 0 else int(ow_len/2)
        ow_mid = minute_len(ow_start) + ow_mid
        ow_mid_str = '%02d:%02d' % (ow_mid // 60, ow_mid % 60)
        
        # Get the data at middle of observable window from ephemerides
        for i in eph['datetime_str', 'RA', 'DEC', 'lunar_elong', 'lunar_illum', 'V', 'RA_rate', 'DEC_rate'] :
            if i[0].split(' ')[1] == ow_mid_str :
                mid_RA, mid_DEC, mid_TOM, mid_Illum, mid_mag, mid_dRA, mid_dDEC = (i[1], i[2], i[3], i[4], i[5], i[6], i[7])

        # Asteroid Motion Time (unit: arcmin)
        fov_w, fov_h = tuple(self.fov.split(' x '))
        # Find Central 25% Central Region in the FOV
        fov_w_25, fov_h_25 = (float(fov_w)/2, float(fov_h)/2)
        # Unit Conversion of Rate (unit: arcsec / hr -> arcmin / hr)
        mid_dRA, mid_dDEC = (mid_dRA / 60, mid_dDEC / 60)

        # Find the |mid_dRA + mid_dDEC|
        mid_vec = math.sqrt(mid_dRA ** 2 + mid_dDEC ** 2)
        mid_vec_angle = math.atan(mid_dDEC/mid_dRA)

        # Find the Diagonal of Central 25% of FOV
        new_fov_h_25 = fov_w_25 * math.tan(mid_vec_angle)
        hypo_fov_25 = math.sqrt(fov_w_25 ** 2 + new_fov_h_25 ** 2)

        # motion time = Diagonal of Central 25% of FOV / Magnitude of Vector Sum
        motion_time = hypo_fov_25 / mid_vec
        motion_time_hour = int(motion_time)
        motion_time_min = int((motion_time - int(motion_time)) * 60)


        # show_results = True if mod = 'info'
        if show_results and not show_both :
            # Print the resulting data
            print('*******************************************************************************')
            print('Target : {}'.format(self.name))
            print('*******************************************************************************')
            print('Telescope Info')
            print('\nName: {}      MPC Code: {}      Camera FOV: {}'.format(self.telescope, self.mpc, self.fov))
            print('\nEvening Nautical Twilight : {} UTC'.format(evening_nt))
            print('30 Deg Rise Time : {} UTC'.format(rise30))
            print('Transit Time  : {} UTC'.format(transit))
            print('30 Deg Set Time  : {} UTC'.format(set30))
            print('Morning Nautical Twilight : {} UTC'.format(morning_nt))
            print('\nObservable Window: {} from {} to {}'.format(ow_len_str, ow_start, ow_end))
            print('Asteroid Motion Time : %02d:%02d' % (motion_time_hour, motion_time_min))
            print('*******************************************************************************')
            print('Asteroid Info')
            print('\nRA : {}'.format(self.RA_sexagesimal(mid_RA)))
            print('DEC : {}'.format(self.DEC_sexagesimal(mid_DEC)))
            print('Target-Obs-Moon Angle : {}'.format(mid_TOM))
            print('Moon Illumination % : {}'.format(mid_Illum))
            print('Visual Magnitude : {}'.format(mid_mag))
            print('*******************************************************************************')

        # show_results = True, show_both = True if mod = 'both'
        elif show_results and show_both :
            # Return resulting values
            print('*******************************************************************************')
            print('Target : {}'.format(self.name))
            print('*******************************************************************************')
            print('Telescope Info')
            print('\nName: {}      MPC Code: {}      Camera FOV: {}'.format(self.telescope, self.mpc, self.fov))
            print('\nEvening Nautical Twilight : {} UTC'.format(evening_nt))
            print('30 Deg Rise Time : {} UTC'.format(rise30))
            print('Transit Time  : {} UTC'.format(transit))
            print('30 Deg Set Time  : {} UTC'.format(set30))
            print('Morning Nautical Twilight : {} UTC'.format(morning_nt))
            print('\nObservable Window: {} from {} to {}'.format(ow_len_str, ow_start, ow_end))
            print('Asteroid Motion Time : %02d:%02d' % (motion_time_hour, motion_time_min))
            print('*******************************************************************************')
            print('Asteroid Info')
            print('\nRA : {}'.format(self.RA_sexagesimal(mid_RA)))
            print('DEC : {}'.format(self.DEC_sexagesimal(mid_DEC)))
            print('Target-Obs-Moon Angle : {}'.format(mid_TOM))
            print('Moon Illumination % : {}'.format(mid_Illum))
            print('Visual Magnitude : {}'.format(mid_mag))
            print('*******************************************************************************')
            self.ow_start = ow_start
            self.ow_end = ow_end

        # show_results = False, show_both = True if mod = 'to text'
        if not show_results and show_both :
            self.f.write('*******************************************************************************\n')
            self.f.write('Target : {}\n'.format(self.name))
            self.f.write('*******************************************************************************\n')
            self.f.write('Telescope Info\n')
            self.f.write('\nName: {}      MPC Code: {}      Camera FOV: {} arcmins\n'.format(self.telescope, self.mpc, self.fov))
            self.f.write('\nEvening Nautical Twilight : {} UTC\n'.format(evening_nt))
            self.f.write('30 Deg Rise Time : {} UTC\n'.format(rise30))
            self.f.write('Transit Time  : {} UTC\n'.format(transit))
            self.f.write('30 Deg Set Time  : {} UTC\n'.format(set30))
            self.f.write('Morning Nautical Twilight : {} UTC\n'.format(morning_nt))
            self.f.write('\nObservable Window: {} from {} to {}\n'.format(ow_len_str, ow_start, ow_end))
            self.f.write('Asteroid Motion Time : %02d:%02d\n' % (motion_time_hour, motion_time_min))
            self.f.write('*******************************************************************************\n')
            self.f.write('Asteroid Info\n')
            self.f.write('\nRA : {}\n'.format(self.RA_sexagesimal(mid_RA)))
            self.f.write('DEC : {}\n'.format(self.DEC_sexagesimal(mid_DEC)))
            self.f.write('Target-Obs-Moon Angle : {}\n'.format(mid_TOM))
            self.f.write('Moon Illumination % : {}\n'.format(mid_Illum))
            self.f.write('Visual Magnitude : {}\n'.format(mid_mag))
            self.f.write('*******************************************************************************\n')
            self.ow_start = ow_start
            self.ow_end = ow_end

        # show_results = False if mod = ephemeris
        else :
            self.ow_start = ow_start
            self.ow_end = ow_end


    # Ephemeris - Prints ephemeris of asteroid
    def ephemeris(self, show_both = False, to_txt = False) :
        # Get Required Values from Info
        if show_both :
            self.info(show_both = True)
        elif to_txt :
            self.info(show_results = False, show_both = True)
        else :
            self.info(show_results = False)

        # Retrieve asteroid data from Horizons
        obj = Horizons(id = self.name, location = self.mpc,
                       epochs = {'start': self.start, 'stop': self.stop,
                                 'step': self.step})

        # Get values: Data & Time, RA, DEC, Alt, AZ, HA
        eph = obj.ephemerides()['datetime_str', 'RA', 'DEC', 'EL', 'AZ', 'hour_angle']

        Alt_format = lambda x: '-%8.4f' % abs(x) if float(x) < 0 else '%8.4f' % abs(x) 
        AZ_format = lambda x: '-%8.4f' % abs(x) if float(x) < 0 else '%8.4f' % abs(x)

        eph['RA'] = [self.RA_sexagesimal(RA) for RA in eph['RA']]
        eph['DEC'] = [self.DEC_sexagesimal(DEC) for DEC in eph['DEC']]
        eph['EL'] = [Alt_format(EL) for EL in eph['EL']]
        eph['AZ'] = [AZ_format(AZ) for AZ in eph['AZ']]
        eph['hour_angle'] = [self.HA_sexagesimal(HA) for HA in eph['hour_angle']]
        
        if to_txt :
            self.f.write('Ephemeris\n\n')
            self.f.write('DATE__(UT)__HR:MN   R.A._____(ICRF)_____DEC   Azi_(a-appr)_Elev   L_AP_Hour_Ang\n')
            self.f.write('*******************************************************************************\n')
            for i in range(1, len(eph)-1) :
                now = eph[i]; h_min = lambda x: ':'.join(self.make_time(x))

                h_min_now = h_min(now[0])
                h_min_start = h_min(self.ow_start)
                h_min_end = h_min(self.ow_end)

                if h_min_now < h_min_start and h_min(eph[i+1][0]) >= h_min_start :
                    self.f.write('>..... Out of Observable Window .....<\n\n')
                elif h_min_now > h_min_end and h_min(eph[i-1][0]) <= h_min_end :
                    self.f.write('\n>..... Out of Observable Window .....<\n')
                elif h_min_now >= h_min_start and h_min_now <= h_min_end :
                    self.f.write('{}   {} {}   {} {}   {}\n'.format(now[0], now[1], now[2], now[3], now[4], now[5]))
            self.f.write('*******************************************************************************')

        else :
            print('Ephemeris\n')
            print('DATE__(UT)__HR:MN   R.A._____(ICRF)_____DEC   Azi_(a-appr)_Elev   L_AP_Hour_Ang')
            print('*******************************************************************************')
            for i in range(1, len(eph)-1) :
                now = eph[i]; h_min = lambda x: ':'.join(self.make_time(x))

                h_min_now = h_min(now[0])
                h_min_start = h_min(self.ow_start)
                h_min_end = h_min(self.ow_end)

                if h_min_now < h_min_start and h_min(eph[i+1][0]) >= h_min_start :
                    print('>..... Out of Observable Window .....<\n')
                elif h_min_now > h_min_end and h_min(eph[i-1][0]) <= h_min_end :
                    print('\n>..... Out of Observable Window .....<')
                elif h_min_now >= h_min_start and h_min_now <= h_min_end :
                    print('{}   {} {}   {} {}   {}'.format(now[0], now[1], now[2], now[3], now[4], now[5]))
            print('*******************************************************************************')
        

    def to_text(self) :
        self.f = open('result.txt', 'w')
        self.ephemeris(to_txt = True)
        self.f.close()

    # Changes RA to Sexagesimal Format
    def RA_sexagesimal(self, RA) :
        h = RA // 15
        m = int((RA / 15) % h * 60)
        s = ((RA / 15) % h * 60 - m) * 60
        return '%d %d %05.2f' % (h, m, s)
    
    # Changes DEC to Sexagesimal Format
    def DEC_sexagesimal(self, DEC) :
        h = int(DEC)
        m = int((DEC - h) * 60)
        s = (((DEC - h) * 60) - m) * 60
        if (h >= 0) and (m >= 0) and (s >= 0) :
            return '+%02d %02d %04.1f' % (abs(h), abs(m), abs(s))
        else :
            return '-%02d %02d %04.1f' % (abs(h), abs(m), abs(s))

    # Changes HA to Sexagesimal Format
    def HA_sexagesimal(self, DEC) :
        h = int(DEC)
        m = int((DEC - h) * 60)
        s = (((DEC - h) * 60) - m) * 60
        if (h >= 0) and (m >= 0) and (s >= 0) :
            return ' %02d %02d %06.3f' % (abs(h), abs(m), abs(s))
        else :
            return '-%02d %02d %06.3f' % (abs(h), abs(m), abs(s))


ObsReq = ObserveRequest()
