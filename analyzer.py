import numpy as np
from matplotlib import pyplot as plt
import os
import json


class RunAnalyzer:

    def __init__(self, shotdir, sclist):
        self.sclist = sclist
        self.shotdir = shotdir
        self.file_list = sorted(os.listdir(self.shotdir))
        self.run_number = os.path.basename(os.path.normpath(shotdir))
        self.shot_number_str = [i.split('_')[1].split('.')[0] for i in self.file_list]
        self.shot_number = np.array(list(map(int, self.shot_number_str)))
        self.shot_data = self.collect_shot_data()
        self.fkeys = self.shot_data[0]['fkeys']
        [freqs, freq_err] = self.collect_freqs_freqerr()
        self.freqs = freqs
        self.freq_err = freq_err
        self.amps = self.collect_amps()
        self.phase_res = self.collect_phase_res()
        self.T2 = self.collect_t2()

    def collect_shot_data(self):
        file_list = self.file_list
        shot_data = []
        for i in range(len(file_list)):
            file_path = os.path.join(self.shotdir, file_list[i])
            with open(file_path, 'r') as read_data:
                print('loading file:' + file_path)
                shot_data.append(json.load(read_data))
        return shot_data

    def collect_freqs_freqerr(self):
        freqs = {}
        freq_err = {}
        for f in self.fkeys:
            freqs[f] = np.array([i['freqs'][f] for i in self.shot_data])
            freq_err[f] = np.array([i['freq_err'][f] for i in self.shot_data])
        return freqs, freq_err

    def collect_t2(self):
        T2 = {}
        keys = ['H', 'N', 'X']
        for k in keys:
            T2[k] = np.array([i['T2'][k] for i in self.shot_data])
        return T2

    def collect_amps(self):
        amps = {}
        new_fkeys = list(set(self.fkeys) - set(['CP']))
        print(new_fkeys)
        for f in new_fkeys:
            print(f)
            for i in range(len(self.shot_data)):
                amps[f] = {}
                amps[f][self.shot_number_str[i]] = np.array(self.shot_data[i]['amps'][f])
        return amps

    def collect_phase_res(self):
        phase_res = {}
        for f in self.fkeys:
            for i in range(len(self.shot_data)):
                phase_res[f] = {}
                phase_res[f][self.shot_number_str[i]] = np.array(self.shot_data[i]['phase_res'][f])
        return phase_res

    def plot_t2(self):
        shot_number = self.shot_number
        T2 = self.T2

        plt.figure(1)
        plt.plot(shot_number, T2['X'], '-x')
        plt.xlabel('shot number')
        plt.ylabel('$T_2$ of Xe [s]')
        plt.title('Run' + self.run_number)

        plt.figure(2)
        plt.plot(shot_number, T2['N'], '-^')
        plt.xlabel('shot number')
        plt.ylabel('$T_2$ of Ne [s]')
        plt.title('Run' + self.run_number)

        plt.figure(3)
        plt.plot(shot_number, T2['H'], '-v')
        plt.xlabel('shot number')
        plt.ylabel('$T_2$ of He [s]')
        plt.title('Run' + self.run_number)
        plt.show()

    def plot_freqs(self):
        shot_number = self.shot_number
        freqs = self.freqs
        freq_err = self.freq_err

        plt.figure()
        plt.errorbar(shot_number, freqs['CP'], yerr=freq_err['CP'], fmt='-o')
        plt.xlabel('shot number')
        plt.ylabel('$\omega_{CP}$')
        plt.title('Run' + self.run_number)

        plt.figure()
        plt.errorbar(shot_number, freqs['H'], yerr=freq_err['H'], fmt='-v')
        plt.xlabel('shot number')
        plt.ylabel('$\omega_{He}$')
        plt.title('Run' + self.run_number)

        plt.figure()
        plt.errorbar(shot_number, freqs['N'], yerr=freq_err['N'], fmt='-^')
        plt.xlabel('shot number')
        plt.ylabel('$\omega_{Ne}$')
        plt.title('Run' + self.run_number)

        plt.figure()
        plt.errorbar(shot_number, freqs['X'], yerr=freq_err['X'], fmt='-x')
        plt.xlabel('shot number')
        plt.ylabel('$\omega_{Xe}$')
        plt.title('Run' + self.run_number)

    def plot_amps(self, a, b):
        shot_number = self.shot_number
        amps = self.amps

        he_amps = [np.mean(amps['H'][i][a:b]) for i in self.shot_number_str]
        ne_amps = [np.mean(amps['N'][i][a:b]) for i in self.shot_number_str]
        xe_amps = [np.mean(amps['X'][i][a:b]) for i in self.shot_number_str]

        plt.figure()
        plt.plot(shot_number, he_amps, '-v', shot_number, ne_amps, '-^', shot_number, xe_amps, '-x')
        plt.legend(['He', 'Ne', 'Xe'])
        plt.xlabel('shot number')
        plt.ylabel('Amplitude [V]')
        plt.show()










