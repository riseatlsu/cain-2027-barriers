"""
Barrier to Resource Usage Analysis

This script analyzes the relationship between learning barriers and the resources
users actually interacted with during their requests (behavioral data), as opposed
to their stated preferences at the end (self-reported data).

Research Question: What resources do users actually interact with when facing
different types of learning barriers?
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

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


def load_interaction_usage_data(data_dir):
    """
    Load request data and count actual resource interactions (what users did).
    
    Returns:
        DataFrame with columns:
        - participant_id
        - request_id
        - barrier_category
        - chat_count: number of chat interactions
        - text_count: number of text (reading) interactions
        - video_count: number of video (watching) interactions
        - total_interactions: total number of all interactions
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
            # Get barrier category from about_request.json
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
            
            # Count interactions by type
            interactions_folder = os.path.join(request_folder, 'interactions')
            interaction_counts = {'chat': 0, 'text': 0, 'video': 0}
            
            if os.path.exists(interactions_folder):
                for interaction_file in os.scandir(interactions_folder):
                    if interaction_file.name.endswith('.json'):
                        with open(interaction_file.path, 'r') as f:
                            interaction_data = json.load(f)
                        
                        interaction_type = interaction_data.get('type', 'unknown')
                        if interaction_type in interaction_counts:
                            interaction_counts[interaction_type] += 1
            
            # Categorize the barrier
            barrier_category = categorize_barrier(learning_barrier)
            
            request_data_list.append({
                'participant_id': participant_id,
                'request_id': request_data.get('request_id', ''),
                'learning_barrier': learning_barrier,
                'barrier_category': barrier_category,
                'chat_count': interaction_counts['chat'],
                'text_count': interaction_counts['text'],
                'video_count': interaction_counts['video'],
                'total_interactions': sum(interaction_counts.values()),
                'created_at': request_data.get('created_at', ''),
                'closed_at': request_data.get('closed_at', '')
            })
    
    df = pd.DataFrame(request_data_list)
    return df


def analyze_resource_usage_by_barrier(df):
    """
    Analyze which resources users actually interacted with based on their barrier type.
    """
    # Define category order
    category_order = ['Design', 'Selection', 'Coordination', 'Use', 'Understanding', 'Information', 'Other']
    
    print("\n")
    print("=" * 80)
    print("BARRIER → ACTUAL RESOURCE USAGE ANALYSIS")
    print("=" * 80)
    print()
    print("Research Question: What resources do users actually interact with")
    print("when facing different types of learning barriers?")
    print("=" * 80)
    print()
    
    # Filter to requests with at least one interaction
    df_with_interactions = df[df['total_interactions'] > 0].copy()
    
    print(f"Total requests: {len(df)}")
    print(f"Requests with at least one resource interaction: {len(df_with_interactions)}")
    print(f"Requests with no interactions: {len(df[df['total_interactions'] == 0])}")
    print()
    
    # Summary statistics by barrier category
    print("=" * 80)
    print("RESOURCE USAGE BY BARRIER CATEGORY")
    print("=" * 80)
    print()
    
    for barrier in category_order:
        barrier_data = df_with_interactions[df_with_interactions['barrier_category'] == barrier]
        
        if len(barrier_data) == 0:
            continue
        
        total_chat = barrier_data['chat_count'].sum()
        total_text = barrier_data['text_count'].sum()
        total_video = barrier_data['video_count'].sum()
        total_all = total_chat + total_text + total_video
        
        avg_chat = barrier_data['chat_count'].mean()
        avg_text = barrier_data['text_count'].mean()
        avg_video = barrier_data['video_count'].mean()
        
        print(f"{barrier} ({len(barrier_data)} requests with interactions)")
        print(f"  Total interactions: {total_all}")
        print(f"    Chat: {total_chat} ({total_chat/total_all*100:.1f}%)")
        print(f"    Text (Read): {total_text} ({total_text/total_all*100:.1f}%)")
        print(f"    Video (Watch): {total_video} ({total_video/total_all*100:.1f}%)")
        print(f"  Average interactions per request:")
        print(f"    Chat: {avg_chat:.2f}")
        print(f"    Text: {avg_text:.2f}")
        print(f"    Video: {avg_video:.2f}")
        print()
    
    # Create summary table
    print("=" * 80)
    print("SUMMARY TABLE: Total Interaction Counts")
    print("=" * 80)
    print()
    
    summary_data = []
    for barrier in category_order:
        barrier_data = df_with_interactions[df_with_interactions['barrier_category'] == barrier]
        
        if len(barrier_data) == 0:
            continue
        
        summary_data.append({
            'Barrier Category': barrier,
            'Requests': len(barrier_data),
            'Chat': barrier_data['chat_count'].sum(),
            'Text': barrier_data['text_count'].sum(),
            'Video': barrier_data['video_count'].sum(),
            'Total': barrier_data['total_interactions'].sum()
        })
    
    summary_df = pd.DataFrame(summary_data)
    print(summary_df.to_string(index=False))
    print()
    
    # Percentage breakdown
    print("=" * 80)
    print("PERCENTAGE BREAKDOWN: Resource Usage Distribution")
    print("(Percentage of total interactions for each barrier)")
    print("=" * 80)
    print()
    
    pct_data = []
    for barrier in category_order:
        barrier_data = df_with_interactions[df_with_interactions['barrier_category'] == barrier]
        
        if len(barrier_data) == 0:
            continue
        
        total = barrier_data['total_interactions'].sum()
        if total > 0:
            pct_data.append({
                'Barrier Category': barrier,
                'Chat %': f"{barrier_data['chat_count'].sum()/total*100:.1f}",
                'Text %': f"{barrier_data['text_count'].sum()/total*100:.1f}",
                'Video %': f"{barrier_data['video_count'].sum()/total*100:.1f}"
            })
    
    pct_df = pd.DataFrame(pct_data)
    print(pct_df.to_string(index=False))
    print()
    
    return df_with_interactions


def analyze_usage_patterns(df):
    """
    Analyze patterns of resource usage across barriers.
    """
    df_with_interactions = df[df['total_interactions'] > 0].copy()
    
    print("=" * 80)
    print("RESOURCE USAGE PATTERNS")
    print("=" * 80)
    print()
    
    # Which resources were used (binary: used or not)
    df_with_interactions['used_chat'] = df_with_interactions['chat_count'] > 0
    df_with_interactions['used_text'] = df_with_interactions['text_count'] > 0
    df_with_interactions['used_video'] = df_with_interactions['video_count'] > 0
    df_with_interactions['num_resource_types'] = (
        df_with_interactions['used_chat'].astype(int) +
        df_with_interactions['used_text'].astype(int) +
        df_with_interactions['used_video'].astype(int)
    )
    
    print("Resource Diversity (number of different resource types used per request):")
    print()
    
    category_order = ['Design', 'Selection', 'Coordination', 'Use', 'Understanding', 'Information', 'Other']
    
    for barrier in category_order:
        barrier_data = df_with_interactions[df_with_interactions['barrier_category'] == barrier]
        
        if len(barrier_data) == 0:
            continue
        
        print(f"{barrier}:")
        print(f"  Avg resource types per request: {barrier_data['num_resource_types'].mean():.2f}")
        
        diversity_counts = barrier_data['num_resource_types'].value_counts().sort_index()
        for num_types, count in diversity_counts.items():
            pct = count / len(barrier_data) * 100
            print(f"    {count} requests used {num_types} type(s) ({pct:.1f}%)")
        print()
    
    # Most common resource combinations
    print("=" * 80)
    print("MOST COMMON RESOURCE COMBINATIONS")
    print("=" * 80)
    print()
    
    for barrier in category_order:
        barrier_data = df_with_interactions[df_with_interactions['barrier_category'] == barrier]
        
        if len(barrier_data) == 0:
            continue
        
        combinations = []
        for _, row in barrier_data.iterrows():
            combo = []
            if row['used_chat']:
                combo.append('Chat')
            if row['used_text']:
                combo.append('Text')
            if row['used_video']:
                combo.append('Video')
            combinations.append('+'.join(combo) if combo else 'None')
        
        combo_counts = pd.Series(combinations).value_counts()
        
        print(f"{barrier} ({len(barrier_data)} requests):")
        for combo, count in combo_counts.head(3).items():
            pct = count / len(barrier_data) * 100
            print(f"  {combo}: {count} ({pct:.1f}%)")
        print()


def create_usage_visualizations(df, output_dir='./'):
    """
    Create visualizations showing actual resource usage by barrier category.
    """
    print("=" * 80)
    print("Creating Visualizations...")
    print("=" * 80)
    print()
    
    df_with_interactions = df[df['total_interactions'] > 0].copy()
    
    if len(df_with_interactions) == 0:
        print("No interaction data available for visualization.")
        return
    
    # Define category order
    category_order = ['Design', 'Selection', 'Coordination', 'Use', 'Understanding', 'Information', 'Other']
    
    # Prepare data for visualization
    viz_data = []
    for barrier in category_order:
        barrier_data = df_with_interactions[df_with_interactions['barrier_category'] == barrier]
        
        if len(barrier_data) == 0:
            continue
        
        viz_data.append({
            'Barrier Category': barrier,
            'Chat': barrier_data['chat_count'].sum(),
            'Text': barrier_data['text_count'].sum(),
            'Video': barrier_data['video_count'].sum()
        })
    
    viz_df = pd.DataFrame(viz_data)
    viz_df = viz_df.set_index('Barrier Category')
    
    # 1. Stacked bar chart (counts)
    fig, ax = plt.subplots(figsize=(12, 8))
    
    viz_df.plot(kind='barh', stacked=True, ax=ax,
                color=['#2E86AB', '#F18F01', '#C73E1D'])
    plt.title('Actual Resource Usage by Barrier Category\n(Total Number of Interactions)',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Number of Interactions', fontsize=11)
    plt.ylabel('Barrier Category', fontsize=11)
    plt.legend(title='Resource Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    stacked_path = os.path.join(output_dir, 'barrier_to_usage_stacked.png')
    plt.savefig(stacked_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {stacked_path}")
    plt.close()
    
    # 2. Percentage breakdown
    fig, ax = plt.subplots(figsize=(12, 8))
    
    viz_df_pct = viz_df.div(viz_df.sum(axis=1), axis=0) * 100
    
    viz_df_pct.plot(kind='barh', stacked=True, ax=ax,
                    color=['#2E86AB', '#F18F01', '#C73E1D'])
    plt.title('Actual Resource Usage by Barrier Category\n(Percentage Distribution)',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Percentage of Interactions', fontsize=11)
    plt.ylabel('Barrier Category', fontsize=11)
    plt.legend(title='Resource Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlim(0, 100)
    
    # Add percentage labels
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f%%', label_type='center', fontsize=8)
    
    plt.tight_layout()
    
    pct_path = os.path.join(output_dir, 'barrier_to_usage_percentage.png')
    plt.savefig(pct_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {pct_path}")
    plt.close()
    
    # 3. Heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(viz_df.T, annot=True, fmt='d', cmap='Blues', ax=ax,
                cbar_kws={'label': 'Number of Interactions'})
    plt.title('Resource Usage Heatmap by Barrier Category',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Barrier Category', fontsize=11)
    plt.ylabel('Resource Type', fontsize=11)
    plt.tight_layout()
    
    heatmap_path = os.path.join(output_dir, 'barrier_to_usage_heatmap.png')
    plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {heatmap_path}")
    plt.close()
    
    print()


def main():
    """
    Main analysis function for resource usage (behavioral data).
    """
    # Get the script directory and find the data folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    data_dir = os.path.join(repo_root, "data")
    
    print("\n")
    print("=" * 80)
    print("BARRIER → ACTUAL RESOURCE USAGE ANALYSIS")
    print("=" * 80)
    print(f"Loading interaction data from: {data_dir}")
    print()
    
    # Load data
    df = load_interaction_usage_data(data_dir)
    
    if df is None or len(df) == 0:
        print("No data found!")
        return
    
    print(f"✓ Loaded {len(df)} requests from {df['participant_id'].nunique()} participants")
    
    # Run analyses
    df_with_interactions = analyze_resource_usage_by_barrier(df)
    analyze_usage_patterns(df)
    
    # Create visualizations
    images_dir = os.path.join(repo_root, "images")
    os.makedirs(images_dir, exist_ok=True)
    create_usage_visualizations(df, output_dir=images_dir)
    
    # Save data
    data_output_dir = os.path.join(repo_root, "data")
    df.to_csv(os.path.join(data_output_dir, 'barrier_to_usage_data.csv'), index=False)
    print(f"✓ Saved detailed data to: {os.path.join(data_output_dir, 'barrier_to_usage_data.csv')}")
    
    print()
    print("=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
