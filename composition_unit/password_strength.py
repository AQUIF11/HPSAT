"""
Created on Mon Feb  8 19:16:24 2021

@author: Aquif R Mir
"""

"""
--COMPOSITION UNIT
password_strength module combines the results of ml_component module
and rule_based_component module to get the final score of a given password string.
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "ml_component"))
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "rule_based_component"))

import ml_password_strength
import rule_based_password_strength


class PasswordStrength:
    def __init__(self, password):
        self.password = password
    
    def get_password_analysis(self):
        ml_ps = ml_password_strength.MLPasswordStrength(self.password)
        rb_ps = rule_based_password_strength.RuleBasedPasswordStrength(self.password)
        
        ml_password_score = ml_ps.get_ml_score()
        rb_password_score = rb_ps.get_score()
        
        # print("Password: {:s}".format(self.password))
        print("Ml Password Classification Score: {:d}".format(ml_password_score))
        print("Rule Based Password Score: {:d}".format(rb_password_score))
        
        results = rb_ps.get_results()
        flags = rb_ps.get_strength_flags()
        
        print("\nCredits:")
        print("Length Score: {:d} ({:d})".format(results["length_score"], flags["length"]))
        print("Lower And Upper Case Character Score: {:d} ({:d}, {:d})".format(results["lower_upper_case_score"], flags["lower_case"], flags["upper_case"]))
        print("Digit Score: {:d} ({:d})".format(results["digits_score"], flags["digits"]))
        print("Special Character Score: {:d} ({:d})".format(results["special_score"], flags["special_chars"]))
        print("Middle Score: {:d} ({:d})".format(results["middle_score"], flags["middle_num_symbol"]))
        print("Extra Score: {:d} ({:d})".format(results["extra_score"], flags["extra"]))
        
        print("\nPenalties")
        print("Letters Only Score: {:d} ({:d})".format(results["letters_only_score"], flags["letters_only"]))
        print("Numbers Only Score: {:d} ({:d})".format(results["numbers_only_score"], flags["numbers_only"]))
        print("Repeating Chars Score: {:d} ({:d})".format(results["repeating_chars_score"], flags["repeating_chars"]))
        print("Consecutive Case Score: {:d} ({:d}, {:d}, {:d})".format(results["consecutive_case_score"], flags["consecutive_lower_case"], flags["consecutive_upper_case"], flags["consecutive_digits"]))
        print("Sequential Letters Score: {:d} ({:d})".format(results["sequential_letters_score"], flags["sequential_letters"]))
        print("Sequential Numbers Score: {:d} ({:d})".format(results["sequential_numbers_score"], flags["sequential_nums"]))
        print("Dictionary Words Score: {:d} ({:d})".format(results["dictionary_words_score"], flags["dictionary_word"]))
        
        # Normalizing both scores to prepare final score
        rb_password_score = rb_password_score if rb_password_score <= 100 else 100
        
        if ml_password_score == 1:
            ml_password_score = 25
        elif ml_password_score == 2:
            ml_password_score = 60
        elif ml_password_score == 3:
            ml_password_score = 100
        
        final_score = (rb_password_score + ml_password_score) / 2
        
        if final_score < 30:
            password_complexity = "Very Weak"
        elif final_score < 50:
            password_complexity = "Weak"
        elif final_score < 70:
            password_complexity = "OK"
        elif final_score < 90:
            password_complexity = "Strong"
        else:
            password_complexity = "Very Strong"
        
        print("\n\nFinal Score: {:f}".format(final_score))
        print("Password Complexity: {:s}".format(password_complexity))
        

def main():
    flag = True
    choice = 1
    
    while flag:
        input_string = input("\nEnter Password: ")
        ps = PasswordStrength(input_string)
        
        ps.get_password_analysis()
        
        choice = int(input("Do you want to continue(1->Yes, 0->No): "))
        
        if not choice:
            flag = False
    
    print("Program Terminated")


if __name__ == "__main__":
    main()


