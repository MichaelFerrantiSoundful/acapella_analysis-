import numpy as np

def timed_vocal_eval(vocal_times, lower_bpm_bound=75, high_bpm_bound=185):
    sub_list = ['1', '2', '4', '8', '16', '4t', '8t']
    close_hit_divisor = 4
    score_dict = {}
    shifted_score_dict= {}
    close_hit_dict = {}
    shifted_close_dict = {}
    # for every subdivision of that bpm (1/8 note, 1/8 note shifted, 1/4, 1/16, triplet 1/8th)
    # given the bpm, subdivion, and index of transient, calculate the score of the nearest bpm marker
    # find what bpm marker the vocal transient is closest to for its given window which
    # window is determined by the subdivision length *2 - 2 centered aroind the same index as the vocal transient
    # abs distance from vocal transiet to closest bpm marker is added to score
    # if score is better than the xth best score for that bpm and subsivion(length of best scores list)
    # add bpm and score to that sub division in the class 2day array
    first_time = True
    i = 0
    for trans_time in vocal_times:
        blocked = False
        trans_time = trans_time * 1000
        for subd in sub_list:
            for bpm in range(lower_bpm_bound, high_bpm_bound + 1):
                subd_length = 240000/(bpm*int(subd[0]))
                if 't' in subd:
                    subd_length = subd_length*(2/3)
                subd_mult = trans_time//subd_length
                first_marker = subd_mult*subd_length
                second_marker = first_marker + subd_length
                if abs(trans_time-first_marker) <= abs(trans_time-second_marker):
                    closest_marker = first_marker
                    if not first_time:
                        blocked = abs(trans_time - first_marker) > abs(vocal_times[i - 1]-first_marker)
                else:
                    closest_marker = second_marker
                    if i + 1 < len(vocal_times):
                        blocked = abs(trans_time - second_marker) > abs(vocal_times[i + 1] - second_marker)
                if first_time:
                    if bpm == lower_bpm_bound:
                        score_dict.update({subd: {bpm: abs(trans_time - closest_marker)}})
                    else:
                        score_dict[subd].update({bpm: abs(trans_time - closest_marker)})
                else:
                    if not blocked:
                        score_dict[subd][bpm] = score_dict[subd][bpm] + (abs(trans_time - closest_marker)*(bpm/100))

                #close hit
                if first_time is True:
                    if bpm == lower_bpm_bound:
                        close_hit_dict.update({subd: {bpm: 0}})
                        shifted_close_dict.update({subd: {bpm: 0}})
                    else:
                        close_hit_dict[subd].update({bpm: 0})
                        shifted_close_dict[subd].update({bpm: 0})
                if not blocked:
                    if abs(trans_time - closest_marker) < (subd_length /close_hit_divisor):
                        close_hit_dict[subd][bpm] = close_hit_dict[subd][bpm] + 1
                #print(subd, bpm)

                #shifted score
                #shifted score algo
                blocked = False
                trans_time_shifted = trans_time
                first_marker = first_marker + (subd_length/2)
                second_marker = second_marker + (subd_length/2)
                if abs(trans_time_shifted - first_marker) <= abs(trans_time_shifted - second_marker):
                    closest_marker = first_marker
                    if not first_time:
                        blocked = abs(trans_time - first_marker) > abs(vocal_times[i - 1]-first_marker)
                else:
                    closest_marker = second_marker
                    if i + 1 < len(vocal_times):
                        blocked = abs(trans_time - second_marker) > abs(vocal_times[i + 1] - second_marker)
                if first_time:
                    if bpm == lower_bpm_bound:
                        shifted_score_dict.update({subd: {bpm: abs(trans_time_shifted - closest_marker)}})
                    else:
                        shifted_score_dict[subd].update({bpm: abs(trans_time_shifted - closest_marker)})
                else:
                    if not blocked:
                        shifted_score_dict[subd][bpm] = shifted_score_dict[subd][bpm] + (abs(trans_time_shifted - closest_marker)*(bpm/100))
                if not blocked:
                    if abs(trans_time_shifted - closest_marker) < (subd_length / close_hit_divisor):
                        shifted_close_dict[subd][bpm] = shifted_close_dict[subd][bpm] + 1
        first_time = False
        i += 1
    #print(score_dict)
    return score_dict, shifted_score_dict, close_hit_dict, shifted_close_dict

#hidden is calulcate scores with array reversed
# def timed_vocal_eval(vocal_times):
#     sub_list = ['2', '4', '8', '16', '4t', '8t']
#     score_dict = {}
#     print("poo")
#     shifted_score_dict= {}
#     # for every subdivision of that bpm (1/8 note, 1/8 note shifted, 1/4, 1/16, triplet 1/8th)
#     # given the bpm, subdivion, and index of transient, calculate the score of the nearest bpm marker
#     # find what bpm marker the vocal transient is closest to for its given window which
#     # window is determined by the subdivision length *2 - 2 centered aroind the same index as the vocal transient
#     # abs distance from vocal transiet to closest bpm marker is added to score
#     # if score is better than the xth best score for that bpm and subsivion(length of best scores list)
#     # add bpm and score to that sub division in the class 2day array
#     first_time = True
#     for trans_time in vocal_times:
#
#         #print(trans_time)
#         trans_time = trans_time * 1000
#         #print(trans_time)
#         #print(trans_time)
#         #need to add score for every transiet
#         for bpm in range(80,159):
#             for subd in sub_list:
#                 #create two branches, one for non triplets and one for triplets, check for t in sub string
#                 #calulate two closest markers to trans_time for given bpm and sub
#                 subd_length = 240000/(bpm*int(subd[0]))
#                 #print(bpm, subd)
#                 #print("subd_length: " + str(subd_length))
#                 if 't' in subd:
#                     subd_length = subd_length*(2/3)
#                 subd_mult = trans_time//subd_length
#                 first_marker = subd_mult*subd_length
#                 second_marker = first_marker + subd_length
#                 if abs(trans_time-first_marker) <= abs(trans_time-second_marker):
#                     closest_marker = first_marker
#                 else:
#                     closest_marker = second_marker
#                 if first_time:
#                     if subd == '2':
#                         #print(trans_time, bpm, subd, closest_marker)
#                         score_dict.update({bpm: {subd: abs(trans_time - closest_marker)}})
#                     else:
#                         #print(trans_time, bpm, subd, closest_marker)
#                         score_dict[bpm].update({subd: abs(trans_time - closest_marker)})
#                 else:
#                     score_dict[bpm][subd] = score_dict[bpm][subd] + abs(trans_time - closest_marker)
#                 #shifted score
#                 trans_time_shifted = trans_time + subd_length/2
#                 subd_mult = trans_time_shifted // subd_length
#                 first_marker = subd_mult * subd_length
#                 second_marker = first_marker + subd_length
#                 if abs(trans_time_shifted - first_marker) <= abs(trans_time_shifted - second_marker):
#                     closest_marker = first_marker
#                 else:
#                     closest_marker = second_marker
#                 if first_time:
#                     if subd == '2':
#                         shifted_score_dict.update({bpm: {subd: abs(trans_time_shifted - closest_marker)}})
#                     else:
#                         shifted_score_dict[bpm].update({subd: abs(trans_time_shifted - closest_marker)})
#                 else:
#                     shifted_score_dict[bpm][subd] = shifted_score_dict[bpm][subd] + abs(trans_time_shifted - closest_marker)
#         first_time = False
#     #print(score_dict)
#     return score_dict, shifted_score_dict

#def add_score(self, score, subdivsion):
    # add to score for this bpm and subdivision to self.best scores and pop the xth bpm with the lowest score

#def untimed_vocal_eval(self, vocal_bin_1d):
    #segment vocal array

def find_best_scores(dict):
    sub_list = ['1', '2', '4', '8', '16', '4t', '8t']
    #sub_list = ['4', '8']
    use_later= 0
    score_ratio_dict ={}
    best_score_list = {}
    for x in sub_list:
        y=1
        while y < 4:
            mini = min(dict[x], key=dict[x].get)
            print(f"{y} best 1/{x} note score: " + str(mini) + " BPM:  Score of " + str(dict[x][mini]))
            if y==1:
                best_score_list.update({x: {mini: (dict[x][mini])}})
            elif y > 1:
                best_score_list[x].update({mini: (dict[x][mini])})
            if y==1:
                best_score = dict[x][mini]
                use_later = mini
            if y==2:
                second_best = dict[x][mini]
            dict[x].pop(mini)
            y += 1

        score_ratio = best_score/second_best
        score_ratio_dict.update({str(x): str(score_ratio)})
        print("Score ratio of: " + str(score_ratio))
        print(" ")
    best_score_ratio = score_ratio_dict[(min(score_ratio_dict, key=score_ratio_dict.get))]
    best_subd = str(min(score_ratio_dict, key=score_ratio_dict.get))
    best_bpm_ratio = list(next(iter(best_score_list[best_subd].items())))#.append(best_score_ratio)
    best_bpm_ratio.insert(0, best_subd)
    best_bpm_ratio.insert(2, float(best_score_ratio))
    #best_bpm[str(best_subd)].append(best_score_ratio)
    #bpm_with_best_score_ratio = {best_subd: best_bpm_ratio}
    print("Best score ratio is 1/" + best_subd + " note at " + str(best_bpm_ratio[1]) + " bpm")
    print(best_score_ratio)
    #print(best_score_list)
    print(best_bpm_ratio)
    print(score_ratio_dict)
    return best_score_list, best_bpm_ratio, score_ratio_dict


def find_best_hit_score(dict):
    sub_list = ['1', '2', '4', '8', '16', '4t', '8t']
    return_dict = {}
    #sub_list = ['4', '8']
    most_hit_bpm = {}
    big_gap_dict = {}
    cur_best_bpm = 0
    # print(dict)
    for x in sub_list:
        y=1
        score_comp = 0
        score_comp2 = 0
        while y < 4:
            mini = max(dict[x], key=dict[x].get)
            print(f"{y} best 1/{x} note score: " + str(mini) + " BPM:  Score of " + str(dict[x][mini]))
            if y == 1:
                return_dict.update({x: {mini: (dict[x][mini])}})
                score_comp = {mini: int(str(dict[x][mini]))}
                cur_best_bpm = mini
            if y > 1:
                return_dict[x].update({mini: (dict[x][mini])})
            if y==2:
                score_comp2 = {mini: int(str(dict[x][mini]))}
                gap_ratio = float(next(iter(score_comp2.items()))[1]) / float(next(iter(score_comp.items()))[1])
                if abs(gap_ratio < .9):
                    print("Big gap of " + str(gap_ratio))
                    print(big_gap_dict)
                    if cur_best_bpm not in big_gap_dict or gap_ratio < float(big_gap_dict[cur_best_bpm][1]):
                        big_gap_dict.update({cur_best_bpm: [x, gap_ratio]})
            dict[x].pop(mini)
            y += 1
        print(" ")
    highest_score = 0
    highest_score_bpm = 0
    for z in sub_list:
        for best_bpm in return_dict[z]:
            if return_dict[z][best_bpm] > highest_score:
                highest_score = return_dict[z][best_bpm]
                highest_score_bpm = best_bpm
    most_hit_bpm.update({highest_score_bpm: highest_score})
    #write code
    #conf_ratio = most_hit_bpm[highest_score_bpm] / (second_highest score
    print(big_gap_dict)
    return return_dict, most_hit_bpm, big_gap_dict#, conf_ratio


def find_repeated_bpm(list_of_scores):
    # for every score list in input, check the nested key values for repeated values
    sub_list = ['1', '2', '4', '8', '16', '4t', '8t']
    #sub_list = ['1', '2', '4', '8', '4t', '8t']
    best_dict = {}
    most_repeated_bpm = {}
    # for i in range(len(list_of_scores)):
    #     del list_of_scores[i]['16']
    for score_list in list_of_scores:
        for subtest in sub_list:
            indexx = 0
            for best_bpm in score_list[subtest]:
                # if indexx == 2:
                #     break
                if best_bpm in best_dict.keys():
                    best_dict.update({best_bpm: best_dict[best_bpm] + 1})
                else:
                    best_dict.update({best_bpm: 1})
                indexx += 1
    trimmed_dict= {x: y for x, y in best_dict.items() if y != 1}

    max_key = max(trimmed_dict, key=trimmed_dict.get)
    most_repeated_bpm = {max_key: trimmed_dict[max_key]}
    return trimmed_dict, most_repeated_bpm


def compute_bpm(repeated_bpms, most_repeated_bpm, close_hit_dict, best_hit_score, shifted_close_hit_dict, best_shift_hit_score, best_score_list,
                best_score_ratio, shifted_best_score_list, best_shifted_score_ratio, score_ratio_dict, shifted_score_ratio_dict, bpm_sub_scores,
                big_gap_dict, shifted_big_gap_dict, list_size = 5):
    sub_list = ['1', '2', '4', '8', '16', '4t', '8t']
    final_dict = {}
    bpm_list = range(70, 200)
    final_score_dict = {}
    for x in bpm_list:
        final_score_dict.update({x: 0})

    # BEST SCORE RATIO REWARD
    #Awarding the points based on if the best ratios are valid or not
    best_score_ratio_gucci, best_shifted_score_ratio_gucci = compute_top_ratio_allow(best_score_ratio, best_shifted_score_ratio, best_score_list, shifted_best_score_list, sub_list)
    #if both are valid
    if best_score_ratio_gucci is True and best_shifted_score_ratio_gucci is True:
        if best_score_ratio[2] < best_shifted_score_ratio[2]:
            final_score_dict[best_score_ratio[1]] = 4 + final_score_dict[best_score_ratio[1]]
            final_score_dict[best_shifted_score_ratio[1]] = 2 + final_score_dict[best_shifted_score_ratio[1]]
        else:
            final_score_dict[best_shifted_score_ratio[1]] = 4 + final_score_dict[best_shifted_score_ratio[1]]
            final_score_dict[best_score_ratio[1]] = 2 + final_score_dict[best_score_ratio[1]]
    #if one is valid or another
    elif best_score_ratio_gucci is True and best_shifted_score_ratio_gucci is False:
        final_score_dict[best_score_ratio[1]] = 4 + final_score_dict[best_score_ratio[1]]
    elif best_score_ratio_gucci is False and best_shifted_score_ratio_gucci is True:
        final_score_dict[best_shifted_score_ratio[1]] = 4 + final_score_dict[best_shifted_score_ratio[1]]

    #Bonus points to valid top scores with ratios lower than .83 and more for below .8
    for subd in sub_list:
        if .83 > float(score_ratio_dict[subd]) > .8:
            if 't' not in subd:
                bpm = next(iter(best_score_list[subd]))
                bpm_range = range(bpm - 2, bpm + 2)
                if (check_for_range_appearance(bpm, bpm_range, best_score_list, shifted_best_score_list, sub_list)) is True:
                    final_score_dict[bpm] = 3.5 + final_score_dict[bpm]
            elif 't' in subd:
                bpm = next(iter(best_score_list[subd]))
                if (check_for_exact_appearance(bpm, best_score_list, shifted_best_score_list, sub_list)) is True:
                    final_score_dict[bpm] = 3.5 + final_score_dict[bpm]
        elif float(score_ratio_dict[subd]) < .8:
            if 't' not in subd:
                bpm = next(iter(best_score_list[subd]))
                bpm_range = range(bpm - 2, bpm + 2)
                if (check_for_range_appearance(bpm, bpm_range, best_score_list, shifted_best_score_list, sub_list)) is True:
                    final_score_dict[bpm] = 10 + final_score_dict[bpm]
            elif 't' in subd:
                bpm = next(iter(best_score_list[subd]))
                if (check_for_exact_appearance(bpm, best_score_list, shifted_best_score_list, sub_list)) is True:
                    final_score_dict[bpm] = 10 + final_score_dict[bpm]
    for subd in sub_list:
        if .83 > float(shifted_score_ratio_dict[subd]) > .8:
            if 't' not in subd:
                bpm = next(iter(shifted_best_score_list[subd]))
                bpm_range = range(bpm - 2, bpm + 2)
                if (check_for_range_appearance(bpm, bpm_range, best_score_list, shifted_best_score_list, sub_list)) is True:
                    final_score_dict[bpm] = 3.5 + final_score_dict[bpm]
            elif 't' in subd:
                bpm = next(iter(shifted_best_score_list[subd]))
                if (check_for_exact_appearance(bpm, best_score_list, shifted_best_score_list, sub_list)) is True:
                    final_score_dict[bpm] = 3.5 + final_score_dict[bpm]
        elif float(shifted_score_ratio_dict[subd]) < .8:
            if 't' not in subd:
                bpm = next(iter(shifted_best_score_list[subd]))
                bpm_range = range(bpm - 2, bpm + 2)
                if (check_for_range_appearance(bpm, bpm_range, best_score_list, shifted_best_score_list, sub_list)) is True:
                    final_score_dict[bpm] = 10 + final_score_dict[bpm]
            elif 't' in subd:
                bpm = next(iter(shifted_best_score_list[subd]))
                if (check_for_exact_appearance(bpm, best_score_list, shifted_best_score_list, sub_list)) is True:
                    final_score_dict[bpm] = 10 + final_score_dict[bpm]

    #REPEATED BPMS
    # Add 1 point for every test in list
    # Add points to most repeated bpms and ties, and then slightly less for those one off
    most_repeated_bpm_num = next(iter(most_repeated_bpm))
    final_score_dict[most_repeated_bpm_num] = 3.6 + final_score_dict[most_repeated_bpm_num]
    for rep_bpm in repeated_bpms:
        final_score_dict.update({int(rep_bpm): 1 + final_score_dict[rep_bpm]})
        if int(rep_bpm == most_repeated_bpm_num):
            continue
        elif repeated_bpms[int(rep_bpm)] == repeated_bpms[most_repeated_bpm_num]:
            final_score_dict.update({int(rep_bpm): 3.6 + final_score_dict[rep_bpm]})
        elif repeated_bpms[int(rep_bpm)] == (repeated_bpms[most_repeated_bpm_num] - 1):
            final_score_dict.update({int(rep_bpm): 2.5 + final_score_dict[rep_bpm]})
        #bonus points if bpm rep score is 5 or higher
        if repeated_bpms[int(rep_bpm)] == 5:
            final_score_dict.update({int(rep_bpm): 2 + final_score_dict[rep_bpm]})
        elif repeated_bpms[int(rep_bpm)] > 5:
            final_score_dict.update({int(rep_bpm): 5 + final_score_dict[rep_bpm]})


    # CLOSE HITS
    # Award to verfied best hit scores
    most_hit_bpm = next(iter(best_hit_score))
    most_shifted_hit_bpm = next(iter(best_shift_hit_score))
    final_score_dict[most_hit_bpm] = 2.7 + final_score_dict[most_hit_bpm]
    final_score_dict[most_shifted_hit_bpm] = 2.7 + final_score_dict[most_shifted_hit_bpm]
    #award verified good ratios
    #award small points to every top hit test???
    for subtest in sub_list:
        #small award to every top score
        cur_hit_bpm = next(iter(close_hit_dict[subtest]))
        final_score_dict[cur_hit_bpm] = .6 + final_score_dict[cur_hit_bpm]
    for subtest in sub_list:
        cur_hit_bpm_shift = next(iter(shifted_close_hit_dict[subtest]))
        final_score_dict[cur_hit_bpm_shift] = .6 + final_score_dict[cur_hit_bpm_shift]
        #bonuss for high ratios
    #loop through gap score dict and verfiy each one and then award points
    for bpm_of_gap in big_gap_dict:
        bpm_gap_ratio = big_gap_dict[bpm_of_gap][1]
        if 't' not in big_gap_dict[bpm_of_gap][0]:
            bpm_range = range(bpm_of_gap - 2, bpm_of_gap + 2)
            if (check_for_range_appearance(bpm_of_gap, bpm_range, close_hit_dict, shifted_close_hit_dict, sub_list)) is True:
                final_score_dict[bpm_of_gap] = (3/(bpm_gap_ratio**3)) + final_score_dict[bpm_of_gap]
        elif 't' in big_gap_dict[bpm_of_gap][0]:
            if (check_for_exact_appearance(bpm_of_gap, close_hit_dict, shifted_close_hit_dict, sub_list)) is True:
                final_score_dict[bpm_of_gap] = (3/(bpm_gap_ratio**2)) + final_score_dict[bpm_of_gap]
    for bpm_of_gap in shifted_big_gap_dict:
        bpm_gap_ratio = shifted_big_gap_dict[bpm_of_gap][1]
        if 't' not in shifted_big_gap_dict[bpm_of_gap][0]:
            bpm_range = range(bpm_of_gap - 2, bpm_of_gap + 2)
            if (check_for_range_appearance(bpm_of_gap, bpm_range, close_hit_dict, shifted_close_hit_dict, sub_list)) is True:
                final_score_dict[bpm_of_gap] = (3/(bpm_gap_ratio**3)) + (final_score_dict[bpm_of_gap])
        elif 't' in shifted_big_gap_dict[bpm_of_gap][0]:
            if (check_for_exact_appearance(bpm_of_gap, close_hit_dict, shifted_close_hit_dict, sub_list)) is True:
                final_score_dict[bpm_of_gap] = (3/(bpm_gap_ratio**2)) + (final_score_dict[bpm_of_gap])

    # Award points if the best score for the subtest, a tad if second best
    # for subtest in sub_list:
    #     first_bpm = next(iter(best_score_list[subtest]))
    #     final_score_dict.update({int(first_bpm): 1 + final_score_dict[first_bpm]})
    #     second_bpm = next(iter(best_score_list[subtest]))
    #     final_score_dict.update({int(second_bpm): .5 + final_score_dict[second_bpm]})
    #     first_bpm_shift = next(iter(shifted_best_score_list[subtest]))
    #     final_score_dict.update({int(first_bpm_shift): 1 + final_score_dict[first_bpm_shift]})
    #     second_bpm_shift = next(iter(shifted_best_score_list[subtest]))
    #     final_score_dict.update({int(second_bpm_shift): .5 + final_score_dict[second_bpm_shift]})

    # if bpm is in the top of its subtest bpm_sub_scores then add 1? maybe not
    # for subtest in sub_list:
    #     cur_hit_bpm = next(iter(best_score_list[subtest]))
    #     final_score_dict[cur_hit_bpm] = .5 + final_score_dict[cur_hit_bpm]
    #     #final_score_list[cur_hit_bpm][1] += .5
    # for subtest in sub_list:
    #     cur_hit_bpm = next(iter(shifted_best_score_list[subtest]))
    #     final_score_dict[cur_hit_bpm] += .5 + final_score_dict[cur_hit_bpm]

    # award additinoal points for combos
         # if bpm has best score especially confident one and is on hot list 1 points

    # find way to sum bpm that are 2x each together (80, 160)
    final_score = max(final_score_dict, key=final_score_dict.get)

    i = 0
    while i < list_size:
        next_final = max(final_score_dict, key=final_score_dict.get)
        value = final_score_dict.pop(next_final)
        final_dict.update({next_final: round(value, 2)})
        i += 1

    return final_score, final_dict


def check_for_range_appearance(bpm, bpm_range, score_list, shifted_score_list, sub_list):
    valid = 0
    #half_list = [x / 2 for x in bpm_range]
    #double_list = [x * 2 for x in bpm_range]
    bpm_range = list(bpm_range)
    bpm_range.extend([bpm/2, bpm*2])
    for subd in sub_list:
        if any(x in bpm_range for x in score_list[subd].keys()):
            valid += 1
        if any(x in bpm_range for x in shifted_score_list[subd].keys()):
            valid += 1
    if valid > 1:
        valid = True
    else:
        valid = False
    return valid


def check_for_exact_appearance(exact_bpm, score_list, shifted_score_list, sub_list, is_t=True):
    valid = 1
    bpm_range = [exact_bpm, exact_bpm/2, exact_bpm*2]
    if is_t is True:
        for subd in sub_list:
            if ('t' not in subd) and (next(iter(score_list[subd])) in bpm_range):
                valid += 1
            if ('t' not in subd) and (next(iter(shifted_score_list[subd])) in bpm_range):
                valid += 1
    if valid > 1:
        valid = True
    else:
        valid = False
    return valid

def compute_top_ratio_allow(best_score_ratio, best_shifted_score_ratio, best_score_list, shifted_best_score_list,sub_list):
    best_score_ratio_gucci = 0
    best_shifted_score_ratio_gucci = 0
    best_ratio_bpm_range = (range(best_score_ratio[1] - 2, best_score_ratio[1] + 2))
    best_shifted_ratio_bpm_range = (range(best_shifted_score_ratio[1] - 2, best_shifted_score_ratio[1] + 2))
    for subd in sub_list:
        # if non t and if +- 2 bpm from best score ratio in keys then add a point
        if ('t' not in best_score_ratio[0]) and any(x in best_ratio_bpm_range for x in best_score_list[subd].keys()):
            best_score_ratio_gucci += 1
        # if non t and if +- 2 bpm from best shifted ratio in keys then add point
        if ('t' not in best_shifted_score_ratio[0]) and any(x in best_shifted_ratio_bpm_range for x in best_score_list[subd].keys()):
            best_shifted_score_ratio_gucci += 1
        # if best ratio is t and if subd isnt t and if exact bpm from best score ratio in keys then add a point
        if ('t' in best_score_ratio[0]) and ('t' not in subd) and (best_score_ratio[1] in best_score_list[subd].keys()):
            best_score_ratio_gucci += 2
        # if best ratio is t and if subd isnt t and if exact bpm from best score ratio in keys then add a point
        if ('t' in best_shifted_score_ratio[0]) and ('t' not in subd) and (best_shifted_score_ratio[1] in best_score_list[subd].keys()):
            best_shifted_score_ratio_gucci += 2
        # if non t and if +- 2 bpm from best score ratio in keys then add a point
        # checking shfited lists
        if ('t' not in best_score_ratio[0]) and any(x in best_ratio_bpm_range for x in shifted_best_score_list[subd].keys()):
            best_score_ratio_gucci += 1
        # if non t and if +- 2 bpm from best shifted ratio in keys then add point
        if ('t' not in best_shifted_score_ratio[0]) and any(x in best_shifted_ratio_bpm_range for x in shifted_best_score_list[subd].keys()):
            best_shifted_score_ratio_gucci += 1
        # if best ratio is t and if subd isnt t and if exact bpm from best score ratio in keys then add a point
        if ('t' in best_score_ratio[0]) and ('t' not in subd) and (best_score_ratio[1] in shifted_best_score_list[subd].keys()):
            best_score_ratio_gucci += 2
        # if best ratio is t and if subd isnt t and if exact bpm from best score ratio in keys then add a point
        if ('t' in best_shifted_score_ratio[0]) and ('t' not in subd) and (best_shifted_score_ratio[1] in shifted_best_score_list[subd].keys()):
            best_shifted_score_ratio_gucci += 2
    # setting to true or false
    if best_score_ratio_gucci > 1:
        best_score_ratio_gucci = True
    else:
        best_score_ratio_gucci = False
    if best_shifted_score_ratio_gucci > 1:
        best_shifted_score_ratio_gucci = True
    else:
        best_shifted_score_ratio_gucci = False

    return best_score_ratio_gucci, best_shifted_score_ratio_gucci

