
import librosa
import numpy as np
import tempo_analysis
import os



class VocalLoad:



    def __init__(self):
        #ask for or provide file path and call load vocal
        self.vocal_times = None
        self.vocal_2d = None
        self.vocal_segments = None
        self.sr = None
        os.chdir("/Users/michaelferranti/PycharmProjects/vocal_bpm_detection/")

        direct = "/Users/michaelferranti/PycharmProjects/vocal_bpm_detection/vocals2"
        filepath = "_ 4-Numb - 110bpm.wav"

        # FOLDER ANALYSIS
        # self.folder_analysis(direct)

        # SINGLE FILE ANALYSIS with verification
        vocal_times, output_bpm = self.file_analysis(filepath, direct)

        # verified = self.verify_bpm(filepath, direct, vocal_times, output_bpm)
        # if verified:
        #     print("BPM of " + str(output_bpm) + " SUCCESFULLY verified")
        # else:
        #     print("BPM of " + str(output_bpm) + " FAILED verification")



        #os.chdir("/Users/michaelferranti/PycharmProjects/vocal2.0/")
        #self.results_comparison("30 with trim.txt", "30 without trim.txt")
    def verify_bpm(self, filepath, direct, vocal_times, output_bpm, trim_len=16):
        #loop_time_sec = loop_len * (output_bpm / 60)
        #loop_time_sec = 60 *  (output_bpm * 4 / loop_len)
        loop_time_sec = (240/output_bpm) * trim_len
        trimmed_vocal_array = [x for x in vocal_times if x < loop_time_sec]
        looped_vocal_array = trimmed_vocal_array
        i=1
        while i < 32:
            next_loop = [x + (i * loop_time_sec) for x in trimmed_vocal_array]
            looped_vocal_array = looped_vocal_array + next_loop
            i += 1
        loop_vocal_times, loop_bpm = self.file_analysis(str("LOOPED  " + filepath), direct, vocal_times=looped_vocal_array)
        if output_bpm == loop_bpm:
            x = True
        else:
            x = False
        return x

    def file_analysis(self, filepath, direct, vocal_times = None):
        if vocal_times is None:
            os.chdir(direct)
            print(filepath)
            vocal_times = self.load_vocal(filepath)
        bpm_sub_scores, shifted_bpm_sub_scores, close_hit, shifted_close = tempo_analysis.timed_vocal_eval(vocal_times)
        print("")
        print("------BEST SCORES---------------------------------------------BEST SCORES------------------")
        print("")
        best_score_list, best_score_ratio, score_ratio_dict = tempo_analysis.find_best_scores(bpm_sub_scores)
        print("")
        print("------BEST SHIFTED SCORES-------------------------------------BEST SHIFTED SCORES---------")
        print("")
        shifted_best_score_list, best_shifted_score_ratio, shifted_score_ratio_dict = tempo_analysis.find_best_scores(shifted_bpm_sub_scores)
        print("")
        print("------MOST CLOSE HITS-----------------------------------------MOST CLOSE HITS-------------")
        print("")
        close_hit_dict, best_hit_score, big_gap_dict = tempo_analysis.find_best_hit_score(close_hit)
        print("")
        print("Close Hit List: " + str(close_hit_dict))
        print("Most Hits: " + str(best_hit_score))

        print("")
        print("------MOST SHIFTED CLOSE HITS---------------------------------MOST SHIFTED CLOSE HITS-----------")
        print("")
        shifted_close_hit_dict, best_shift_hit_score, shifted_big_gap_dict = tempo_analysis.find_best_hit_score(shifted_close)
        print("")
        print("Shift Hit List: " + str(shifted_close_hit_dict))
        print("CLose Hits: " + str(best_shift_hit_score))

        input_list = [best_score_list, shifted_best_score_list]
        repeated_bpms, most_repeated_bpm = tempo_analysis.find_repeated_bpm(input_list)
        print("")
        print("------REPEATED BPMS------------------------------------------REPEATED BPMS---------")
        print(repeated_bpms)
        print("Most repeated bpm: " + str(most_repeated_bpm))

        print("------RESULT----------------------RESULT--------------------RESULT---------")
        final_score, final_dict = tempo_analysis.compute_bpm(repeated_bpms, most_repeated_bpm, close_hit_dict,
                                                            best_hit_score, shifted_close_hit_dict,
                                                            best_shift_hit_score,
                                                            best_score_list, best_score_ratio, shifted_best_score_list,
                                                            best_shifted_score_ratio, score_ratio_dict, shifted_score_ratio_dict, bpm_sub_scores, big_gap_dict, shifted_big_gap_dict)
        print("The Bpm of " + str(filepath) + " is " + str(final_score))
        print(final_score)
        print(final_dict)
        return vocal_times, final_score

    def folder_analysis(self, direct):
        list_of_ans = []
        os.chdir(direct)
        for filepath in os.listdir(direct):
            if filepath == ".DS_Store":
                continue
            print(filepath)
            vocal_times = self.load_vocal(filepath)
            bpm_sub_scores, shifted_bpm_sub_scores, close_hit, shifted_close = tempo_analysis.timed_vocal_eval(vocal_times)
            print("")
            print("------BEST SCORES---------------------------------------------BEST SCORES------------------")
            print("")
            best_score_list, best_score_ratio, score_ratio_dict = tempo_analysis.find_best_scores(bpm_sub_scores)
            print("")
            print("------BEST SHIFTED SCORES-------------------------------------BEST SHIFTED SCORES---------")
            print("")
            shifted_best_score_list, best_shifted_score_ratio, shifted_score_ratio_dict = tempo_analysis.find_best_scores(shifted_bpm_sub_scores)
            print("")
            print("------MOST CLOSE HITS-----------------------------------------MOST CLOSE HITS-------------")
            print("")
            close_hit_dict, best_hit_score, big_gap_dict = tempo_analysis.find_best_hit_score(close_hit)
            print("")
            print("Close Hit List: " + str(close_hit_dict))
            print("Most Hits: " + str(best_hit_score))

            print("")
            print("------MOST SHIFTED CLOSE HITS---------------------------------MOST SHIFTED CLOSE HITS-----------")
            print("")
            shifted_close_hit_dict, best_shift_hit_score, shifted_big_gap_dict = tempo_analysis.find_best_hit_score(shifted_close)
            print("")
            print("Shift Hit List: " + str(shifted_close_hit_dict))
            print("CLose Hits: " + str(best_shift_hit_score))

            input_list = [best_score_list, shifted_best_score_list]
            repeated_bpms, most_repeated_bpm = tempo_analysis.find_repeated_bpm(input_list)
            print("")
            print("------REPEATED BPMS------------------------------------------REPEATED BPMS---------")
            print(repeated_bpms)
            print("Most repeated bpm: " + str(most_repeated_bpm))

            print("------RESULT----------------------RESULT--------------------RESULT---------")
            final_score, final_dict = tempo_analysis.compute_bpm(repeated_bpms, most_repeated_bpm, close_hit_dict,
                                                                best_hit_score, shifted_close_hit_dict,
                                                                best_shift_hit_score,
                                                                best_score_list, best_score_ratio, shifted_best_score_list,
                                                                best_shifted_score_ratio, score_ratio_dict, shifted_score_ratio_dict,
                                                                 bpm_sub_scores, big_gap_dict, shifted_big_gap_dict)
            print("The Bpm of " + str(filepath) + " is " + str(final_score))
            print(final_score)
            print(final_dict)
            list_of_ans.append([[filepath, final_score, final_dict]])

        os.chdir("/Users/michaelferranti/PycharmProjects/vocal_bpm_detection/")
        with open('test results/file.txt', 'w') as file:
            for row in list_of_ans:
                file.write(' '.join([str(item) for item in row]))
                file.write('\n')

    # load vocal from file path and return 2d numpy array
    def load_vocal(self, filename):
        #load with librosa from file path and return 2d numpy array
        self.vocal_2d, self.sr = librosa.load(filename)
        #add logic to start at first transient (delete empty space at head of vocal)
        self.vocal_2d, x = librosa.effects.trim(self.vocal_2d)
        vocal_times = self.vocal_to_transient(self.vocal_2d, self.sr)
        return vocal_times

    def vocal_to_transient(self, vocal_2d, sr):
        #onset_frames = librosa.onset.onset_detect(self.vocal_2d, sr=sr, wait=1, pre_avg=1, post_avg=1, pre_max=1, post_max=1)
        o_env = librosa.onset.onset_strength(y=self.vocal_2d, sr=sr, aggregate=np.median, fmax=8000, n_mels=256)
        times = librosa.times_like(o_env, sr=sr)
        onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)
        #vocal_times = librosa.frames_to_time(onset_frames)
       # print(len(vocal_times))
        #onset_frames = librosa.onset.onset_detect(self.vocal_2d, sr=sr)
        vocal_times = librosa.frames_to_time(onset_frames)
        #print(vocal_times)
       # vocal_times = [x - vocal_times[0] for x in vocal_times]
       # vocal_times.pop(0)
        #print(vocal_times)
        #print(len(vocal_times))

        return vocal_times


