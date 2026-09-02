import pandas as pd
import os
import glob


def combine_csv_files(input_directory, output_file):
    # Use glob to find all CSV files in the directory
    csv_files = glob.glob(os.path.join(input_directory, '*.csv'))

    # List to hold dataframes
    dataframes = []

    for csv_file in csv_files:
        try:
            # Read each CSV file into a DataFrame
            df = pd.read_csv(csv_file)
            # Append DataFrame to the list
            dataframes.append(df)
            print(f"Loaded {csv_file}")
        except Exception as e:
            print(f"Failed to load {csv_file}: {e}")

    # Concatenate all DataFrames in the list into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    # Save the combined DataFrame to a new CSV file
    combined_df.to_csv(output_file, index=False)
    print(f"Combined CSV has been saved to {output_file}")


if __name__ == "__main__":
    # Specify the directory containing CSV files
    input_directory = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/csv"
    # Specify the path to the output combined CSV file
    output_file = "/Users/enshanchen/Downloads/for_design_vocabulary_principles/combined.csv"

    # Combine CSV files
    combine_csv_files(input_directory, output_file)
