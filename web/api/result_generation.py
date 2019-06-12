def generate_lm_result(ret_list):
    ret_text = ""
    for ret in ret_list:
        sentence = ret['sentence']
        candidates = ret['candidates']
        raw_word = candidates[0]['raw_word']
        new_word = candidates[0]['candidate']
        position = ret['position_in_sentence']
        ret_text += "%s %s (%d) -> %s\n" % (sentence, raw_word, position, new_word)
    return ret_text


def generate_dep_result(ret_list):
    ret_text = ""
    for ret in ret_list:
        sentence = ret['text']
        mistakes = ret['mistakes']
        possible_mistakes_text = ""
        for mistakes_per_type in mistakes:
            for mistake_info in mistakes_per_type:
                possible_mistakes_text += "%s(%d) " % (mistake_info[0][0], mistake_info[0][1])
        ret_text += "%s     POSSIBLE WORDS: %s\n" % (sentence, possible_mistakes_text)
    return ret_text
