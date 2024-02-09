import pandas as pd
import sys


def main(df, target):

    # Convert GPA to float, and fix nulls
    df['GPA_clean'] = df.GPA.str.extract(r'(\d+.\d+)').astype(float)
    df_gpa_mean = df.GPA_clean.mean()
    df.GPA_clean = df.GPA_clean.fillna(df_gpa_mean)

    # Create dummy columns
    genders = pd.get_dummies(df.Gender, prefix='gender')
    employment = pd.get_dummies(df.employment, prefix='employ')
    fe = pd.get_dummies(df.father_education, prefix='father')

    # Filter df to include only selected columns
    keep_cols = ['income', 'healthy_feeling', 'life_rewarding']
    df_final = df[keep_cols]
    df_final = pd.concat((df_final, genders, employment, fe), axis=1)

    # Remove any remaining nulls
    df_final = df_final.dropna()

    # Save to disk
    df_final.to_csv(target, index=False)


if __name__ == '__main__':
    # Get the filename of the raw data
    source_file = sys.argv[1]
    source_name = source_file.split('.')[0]

    # Build the path to the output directory
    target_location = 'output/' + source_name + '_clean.csv'

    unclean_df = pd.read_csv(source_file)
    main(unclean_df, target_location)
