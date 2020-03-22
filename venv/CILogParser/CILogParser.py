import re
from config import Config


class LogParser:

    def __init__(self):
        self.reg_pattern_name = u'[^\W\d][\w_]*$'
        if Config.INCLUDE_ALL_TESTCASE:
            self.line_match_pattern_entry=u'.*\[.*\]ENTER'
            self.line_match_pattern_exit = u'.*\[.*\]EXIT'
        else:
            self.line_match_pattern_entry=u'\[.*\]ENTER'
            self.line_match_pattern_exit = u'\[.*\]EXIT'
        return None

    def generate_dict(self,txt):
        """
        Generated dictionary on the incoming log data
        :param txt: log texts read from uploaded file
        :return: parsed dict values
        """
        dict_values = []
        for line in txt:
            #Check if ENTER and EXIT texts  are present in the current line
            if re.match(string=line, pattern=self.line_match_pattern_entry):
                operation='ENTRY'
            elif re.match(string=line, pattern=self.line_match_pattern_exit):
                operation='EXIT'
            else:
                continue # Go to next line if ENTER and EXIT texts are missing

            if dict_values:
                yield dict_values

            #extract texts from the lines
            subtxt = line.split(":")
            name_txt = subtxt[2].split(' ')

            #check if name is valid based on given rules
            if re.match(string=name_txt[-1],pattern=self.reg_pattern_name,flags=re.U):
                name = name_txt[-1].strip()
            else:
                name = "anonymous"

            #putting it all together
            dict_values = {
                "operation": operation,
                "filename": subtxt[1].strip(),
                "line_number": name_txt[0],
                "name": name
            }
        yield dict_values