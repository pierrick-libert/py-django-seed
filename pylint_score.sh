#!/bin/bash
threshold=9.0

# Run pylint and output to both file and console
python -m pylint --load-plugins pylint_django --disable=duplicate-code *.py **/*.py | tee pylint_report.txt

# Extract the score from the pylint output
score=$(tail -n2 pylint_report.txt | grep -Po '(?<=Your code has been rated at )[-+]?[0-9]*\.?[0-9]+(?=/10)')

echo "Score is $score"

# Check if the score is below the threshold and exit with an error status if it is
if python -c "import sys; is_error=float('$score') < float('$threshold'); sys.exit(0 if is_error else 1)"; then
    echo "Pylint score is $score, which is below the threshold of $threshold. Exiting with error."
    exit 1
else
    echo "Pylint score is $score, which is above the threshold of $threshold. No errors."
fi
