import argparse
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='Convert Excel test matrix to CSV for agent use.')
    parser.add_argument('input_xlsx', help='Path to the Excel file')
    parser.add_argument('output_csv', help='Path to write the CSV file')
    args = parser.parse_args()

    df = pd.read_excel(args.input_xlsx, dtype=str)
    df.to_csv(args.output_csv, index=False, encoding='utf-8')
    print(f'Converted {args.input_xlsx} to {args.output_csv}')


if __name__ == '__main__':
    main()
