"""
Barrier to Time Spent Analysis

This script analyzes the relationship between learning barriers and the amount
of time users spent working on their requests.

Research Question: How does the time spent on a request relate to the type
of learning barrier a user is facing?
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set style for visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


def categorize_barrier(barrier_text):
    """
    Map specific barrier descriptions to standardized barrier categories.
    
    These barriers are adapted from Ko et al. (2004) learning barrier framework,
    with "computer" changed to "robot" for this study.
    """
    if not barrier_text or pd.isna(barrier_text):
        return 'Other'
    
    # Normalize: lowercase, strip whitespace, and normalize apostrophes
    # Data uses curly apostrophes (U+2019 ') not straight apostrophes (U+0027 ')
    normalized = barrier_text.lower().strip()
    # Replace curly apostrophes (both U+2018 and U+2019) with straight ones
    normalized = normalized.replace('\u2019', "'").replace('\u2018', "'")
    
    # Design: "I don't know what I want the robot to do…"
    if "i don't know what i want the robot to do" in normalized:
        return 'Design'
    
    # Selection: "I think I know what I want the robot to do, but I don't know what to use…"
    elif "i think i know what i want the robot to do" in normalized and "don't know what to use" in normalized:
        return 'Selection'
    
    # Coordination: "I think I know what things to use, but I don't know how to make them work together…"
    elif "i think i know what things to use" in normalized and "don't know how to make them work together" in normalized:
        return 'Coordination'
    
    # Use: "I think I know what to use, but I don't know how to use it…"
    elif "i think i know what to use" in normalized and "don't know how to use it" in normalized:
        return 'Use'
    
    # Understanding: "I thought I knew how to use this, but it didn't do what I expected…"
    elif "i thought i knew how to use this" in normalized and "didn't do what i expected" in normalized:
        return 'Understanding'
    
    # Information: "I think I know why it didn't do what I expected, but I don't know how to check…"
    elif "i think i know why" in normalized and "didn't do what i expected" in normalized and "don't know how to check" in normalized:
        return 'Information'
    
    # Everything else goes to "Other"
    else:
        return 'Other'


def parse_datetime(datetime_str):
    """Parse datetime string in format MM/DD/YYYY HH:MM:SS"""
    try:
        return datetime.strptime(datetime_str, "%m/%d/%Y %H:%M:%S")
    except:
        return None


def load_time_data(data_dir):
    """
    Load request data with time information.
    
    Returns:
        DataFrame with columns:
        - participant_id
        - request_id
        - barrier_category
        - created_at
        - closed_at
        - duration_minutes: time spent on request in minutes
        - duration_hours: time spent on request in hours
    """
    interaction_folder = os.path.join(data_dir, "interactions")
    
    if not os.path.exists(interaction_folder):
        print(f"Error: Directory {interaction_folder} not found")
        return None
    
    request_data_list = []
    
    # Iterate through all participant folders
    participant_folders = [f.path for f in os.scandir(interaction_folder) if f.is_dir()]
    
    for participant_folder in participant_folders:
        participant_id = os.path.basename(participant_folder)
        requests_subfolder = os.path.join(participant_folder, 'requests')
        
        if not os.path.isdir(requests_subfolder):
            continue
        
        # Process all requests for this participant
        request_folders = [f.path for f in os.scandir(requests_subfolder) if f.is_dir()]
        
        for request_folder in request_folders:
            about_request_path = os.path.join(request_folder, 'about_request.json')
            
            if not os.path.exists(about_request_path):
                continue
            
            with open(about_request_path, 'r') as f:
                request_data = json.load(f)
            
            # Get the learning barrier (with correction if needed)
            initial_category = request_data.get('category', 'Unknown')
            feedback = request_data.get('feedback', [])
            
            if feedback and len(feedback) > 0:
                was_category_correct = feedback[0].get('was_category_correct', None)
                
                if was_category_correct == "No" and 'category' in feedback[0]:
                    learning_barrier = feedback[0]['category']
                else:
                    learning_barrier = initial_category
            else:
                learning_barrier = initial_category
            
            # Parse timestamps
            created_str = request_data.get('created_at', '')
            closed_str = request_data.get('closed_at', '')
            
            created_dt = parse_datetime(created_str)
            closed_dt = parse_datetime(closed_str)
            
            # Calculate duration
            duration_minutes = None
            duration_hours = None
            
            if created_dt and closed_dt:
                duration_delta = closed_dt - created_dt
                duration_minutes = duration_delta.total_seconds() / 60
                duration_hours = duration_minutes / 60
            
            # Categorize the barrier
            barrier_category = categorize_barrier(learning_barrier)
            
            request_data_list.append({
                'participant_id': participant_id,
                'request_id': request_data.get('request_id', ''),
                'learning_barrier': learning_barrier,
                'barrier_category': barrier_category,
                'created_at': created_str,
                'closed_at': closed_str,
                'duration_minutes': duration_minutes,
                'duration_hours': duration_hours
            })
    
    df = pd.DataFrame(request_data_list)
    return df


def analyze_time_by_barrier(df):
    """
    Analyze time spent on requests by barrier category.
    """
    # Define category order
    category_order = ['Design', 'Selection', 'Coordination', 'Use', 'Understanding', 'Information', 'Other']
    
    print("\n")
    print("=" * 80)
    print("BARRIER → TIME SPENT ANALYSIS")
    print("=" * 80)
    print()
    print("Research Question: How does the time spent on a request relate to")
    print("the type of learning barrier a user is facing?")
    print("=" * 80)
    print()
    
    # Filter to requests with valid time data
    df_with_time = df[df['duration_minutes'].notna()].copy()
    
    print(f"Total requests: {len(df)}")
    print(f"Requests with valid time data: {len(df_with_time)}")
    print(f"Requests without time data: {len(df[df['duration_minutes'].isna()])}")
    print()
    
    # Overall statistics
    print("=" * 80)
    print("OVERALL TIME STATISTICS")
    print("=" * 80)
    print()
    print(f"Mean duration: {df_with_time['duration_minutes'].mean():.1f} minutes ({df_with_time['duration_hours'].mean():.2f} hours)")
    print(f"Median duration: {df_with_time['duration_minutes'].median():.1f} minutes ({df_with_time['duration_hours'].median():.2f} hours)")
    print(f"Std deviation: {df_with_time['duration_minutes'].std():.1f} minutes")
    print(f"Min duration: {df_with_time['duration_minutes'].min():.1f} minutes")
    print(f"Max duration: {df_with_time['duration_minutes'].max():.1f} minutes ({df_with_time['duration_hours'].max():.2f} hours)")
    print()
    
    # Statistics by barrier category
    print("=" * 80)
    print("TIME SPENT BY BARRIER CATEGORY")
    print("=" * 80)
    print()
    
    summary_data = []
    
    for barrier in category_order:
        barrier_data = df_with_time[df_with_time['barrier_category'] == barrier]
        
        if len(barrier_data) == 0:
            continue
        
        mean_min = barrier_data['duration_minutes'].mean()
        median_min = barrier_data['duration_minutes'].median()
        std_min = barrier_data['duration_minutes'].std()
        min_min = barrier_data['duration_minutes'].min()
        max_min = barrier_data['duration_minutes'].max()
        
        print(f"{barrier} ({len(barrier_data)} requests)")
        print(f"  Mean: {mean_min:.1f} min ({mean_min/60:.2f} hrs)")
        print(f"  Median: {median_min:.1f} min ({median_min/60:.2f} hrs)")
        print(f"  Std Dev: {std_min:.1f} min")
        print(f"  Range: {min_min:.1f} - {max_min:.1f} min ({min_min/60:.2f} - {max_min/60:.2f} hrs)")
        print()
        
        summary_data.append({
            'Barrier Category': barrier,
            'N': len(barrier_data),
            'Mean (min)': f"{mean_min:.1f}",
            'Median (min)': f"{median_min:.1f}",
            'Std Dev (min)': f"{std_min:.1f}",
            'Min (min)': f"{min_min:.1f}",
            'Max (min)': f"{max_min:.1f}"
        })
    
    # Summary table
    print("=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print()
    
    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))
    print()
    
    # Time distribution analysis
    print("=" * 80)
    print("TIME DISTRIBUTION")
    print("=" * 80)
    print()
    
    # Define time buckets
    df_with_time['time_bucket'] = pd.cut(
        df_with_time['duration_minutes'],
        bins=[0, 10, 20, 30, 60, float('inf')],
        labels=['0-10 min', '10-20 min', '20-30 min', '30-60 min', '60+ min']
    )
    
    for barrier in category_order:
        barrier_data = df_with_time[df_with_time['barrier_category'] == barrier]
        
        if len(barrier_data) == 0:
            continue
        
        bucket_counts = barrier_data['time_bucket'].value_counts().sort_index()
        
        print(f"{barrier} ({len(barrier_data)} requests):")
        for bucket, count in bucket_counts.items():
            pct = count / len(barrier_data) * 100
            print(f"  {bucket}: {count} ({pct:.1f}%)")
        print()
    
    return df_with_time


def create_time_visualizations(df, output_dir='./'):
    """
    Create visualizations showing time spent by barrier category.
    """
    print("=" * 80)
    print("Creating Visualizations...")
    print("=" * 80)
    print()
    
    df_with_time = df[df['duration_minutes'].notna()].copy()
    
    if len(df_with_time) == 0:
        print("No time data available for visualization.")
        return
    
    # Define category order
    category_order = ['Design', 'Selection', 'Coordination', 'Use', 'Understanding', 'Information', 'Other']
    
    # Filter to categories present in data
    present_categories = [cat for cat in category_order if cat in df_with_time['barrier_category'].values]
    
    # 1. Box plot - Time distribution by barrier
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Prepare data for box plot
    plot_data = df_with_time[df_with_time['barrier_category'].isin(present_categories)]
    
    # Create box plot with ordered categories
    order_for_plot = [cat for cat in category_order if cat in present_categories]
    sns.boxplot(data=plot_data, y='barrier_category', x='duration_minutes', 
                order=order_for_plot, ax=ax, palette='Set2')
    
    plt.title('Time Spent on Requests by Barrier Category\n(Distribution)',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Duration (minutes)', fontsize=11)
    plt.ylabel('Barrier Category', fontsize=11)
    plt.tight_layout()
    
    boxplot_path = os.path.join(output_dir, 'barrier_to_time_boxplot.png')
    plt.savefig(boxplot_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {boxplot_path}")
    plt.close()
    
    # 2. Bar chart - Mean time by barrier
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Calculate means
    mean_times = []
    for barrier in order_for_plot:
        barrier_data = df_with_time[df_with_time['barrier_category'] == barrier]
        mean_times.append(barrier_data['duration_minutes'].mean())
    
    bars = ax.barh(order_for_plot, mean_times, color='#2E86AB')
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        ax.text(width, bar.get_y() + bar.get_height()/2, 
                f'{width:.1f} min',
                ha='left', va='center', fontsize=10, fontweight='bold')
    
    plt.title('Mean Time Spent by Barrier Category',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Mean Duration (minutes)', fontsize=11)
    plt.ylabel('Barrier Category', fontsize=11)
    plt.tight_layout()
    
    barplot_path = os.path.join(output_dir, 'barrier_to_time_mean.png')
    plt.savefig(barplot_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {barplot_path}")
    plt.close()
    
    # 3. Violin plot - Time distribution with density
    fig, ax = plt.subplots(figsize=(12, 8))
    
    sns.violinplot(data=plot_data, y='barrier_category', x='duration_minutes',
                   order=order_for_plot, ax=ax, palette='muted')
    
    plt.title('Time Spent Distribution by Barrier Category\n(Violin Plot)',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Duration (minutes)', fontsize=11)
    plt.ylabel('Barrier Category', fontsize=11)
    plt.tight_layout()
    
    violin_path = os.path.join(output_dir, 'barrier_to_time_violin.png')
    plt.savefig(violin_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {violin_path}")
    plt.close()
    
    print()


def main():
    """
    Main analysis function for time spent on requests.
    """
    # Get the script directory and find the data folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    data_dir = os.path.join(repo_root, "data")
    
    print("\n")
    print("=" * 80)
    print("BARRIER → TIME SPENT ANALYSIS")
    print("=" * 80)
    print(f"Loading data from: {data_dir}")
    print()
    
    # Load data
    df = load_time_data(data_dir)
    
    if df is None or len(df) == 0:
        print("No data found!")
        return
    
    print(f"✓ Loaded {len(df)} requests from {df['participant_id'].nunique()} participants")
    
    # Run analysis
    df_with_time = analyze_time_by_barrier(df)
    
    # Create visualizations
    images_dir = os.path.join(repo_root, "images")
    os.makedirs(images_dir, exist_ok=True)
    create_time_visualizations(df, output_dir=images_dir)
    
    # Save data
    data_output_dir = os.path.join(repo_root, "data")
    df.to_csv(os.path.join(data_output_dir, 'barrier_to_time_data.csv'), index=False)
    print(f"✓ Saved detailed data to: {os.path.join(data_output_dir, 'barrier_to_time_data.csv')}")
    
    print()
    print("=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
