from detailedDesign.detailDesign import detail_design
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--make_stability",  type=bool, default=False)
    args = parser.parse_args()
    input_opt = args.make_stability
    # try:
    # except:
        # print("import not found")
    detail_design(debug=False, make_stability=input_opt)


#       /\_/\
#  /\  / o o \
# //\\ \~(*)~/
# `  \/   ^ /
#    | \|| ||  Lara
#    \ '|| ||  Allen
#     \)()-())
# The cat ascii art of truth
#-
