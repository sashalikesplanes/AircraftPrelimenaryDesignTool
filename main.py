from detailedDesign.detailDesign import detail_design
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--make-stability",  type=bool, default=False)
    parser.add_argument("--stress", type=bool, default=False)
    args = parser.parse_args()
    make_stability = args.make_stability
    stress = args.stress
    detail_design(debug=False, make_stability=make_stability, stress=stress)

#       /\_/\
#  /\  / o o \
# //\\ \~(*)~/
# `  \/   ^ /
#    | \|| ||  Lara
#    \ '|| ||  Allen
#     \)()-())
# The cat ascii art of truth
