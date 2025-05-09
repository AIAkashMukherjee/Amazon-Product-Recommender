import pandas as pd
import re
import os

def load_data(file_path):
    """Load merged CSV file into DataFrame"""
    return pd.read_csv(file_path)

def clean_price(price):
    """Clean price column: remove currency symbols and commas"""

    price = re.sub(r'[^\d.]', '', str(price))  # Keep only digits and dot
    try:
        return float(price)
    except ValueError:
        return 0.0

def clean_rating(rating):
    """Extract numeric rating"""

    match = re.search(r'(\d+(\.\d+)?)', str(rating))
    return float(match.group(1)) if match else 0.0

def clean_reviews(reviews):
    """Extract numeric number of reviews"""

    reviews = re.sub(r'[^\d]', '', str(reviews))  # Remove non-digits
    return int(reviews) if reviews else 0

def clean_text(text):
    """Basic text cleaning"""

    text = str(text).strip()
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single
    return text

def clean_availability(value):
    value = str(value).lower()
    if any(keyword in value for keyword in ['only', 'available', 'in stock']):
        return 'In stock'
    else:
        return 'Not Available'
    
def clean_category(cat):
    # Remove amazon_ and _data
    cat = str(cat)
    cat = cat.replace('amazon_', '').replace('_data', '')
    return cat.strip()    

def clean_dataframe(df):
    """Apply cleaning functions to the whole DataFrame"""
    
    # Clean price, rating, reviews
    if 'price' in df.columns:
        df['price'] = df['price'].apply(clean_price)
    
    if 'rating' in df.columns:
        df['rating'] = df['rating'].apply(clean_rating)
    
    if 'reviews' in df.columns:
        df['reviews'] = df['reviews'].apply(clean_reviews)
    
    # Clean title and description
    if 'title' in df.columns:
        df['title'] = df['title'].apply(clean_text)
    
    if 'description' in df.columns:
        df['description'] = df['description'].apply(clean_text)

    if 'availability' in df.columns:
        df['availability'] = df['availability'].apply(clean_availability)

    # Clean category
    if 'Category' in df.columns:
        df['Category'] = df['Category'].apply(clean_category)    
    
    # Remove duplicates by title
    df.drop_duplicates(subset=['title'], inplace=True)

    # Drop rows where price or title is missing/empty
    df = df[~df['title'].isnull() & (df['title'].str.strip() != "")]
    df = df[~df['price'].isnull()]

    # Final cleanup: drop any row with any null (force no empty rows)
    # df.dropna(inplace=True)
    
    return df

def save_clean_data(df, save_path):
    """Save cleaned DataFrame to CSV"""
    df.to_csv(save_path, index=False)
    print(f"✅ Cleaned data saved to {save_path}")

def main():
    # Input and output paths
    raw_file_path = 'artifacts/data/raw_data.csv'
    clean_file_path = 'artifacts/data/cleaned_data.csv'
    
    # Load
    df = load_data(raw_file_path)
    print(f"📥 Loaded data: {df.shape[0]} rows")
    
    # Clean
    df_clean = clean_dataframe(df)
    print(f"🧹 Cleaned data: {df_clean.shape[0]} rows (no nulls, no blanks)")
    
    # Save
    save_clean_data(df_clean, clean_file_path)

if __name__ == "__main__":
    main()
