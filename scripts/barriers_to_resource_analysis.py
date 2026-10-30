"""
Analysis script to examine the relationship between learning barriers and 
the type of resource participants found most useful.

Research Question: What type of learning material does a person prefer based on 
the type of learning barrier they are facing?

Data Mapping:
- 'category' field in about_request.json = Learning barrier (reported at START)
- 'most_useful_category' in feedback = Resource type found most useful (reported at END)
- Barriers are categorized into standard types: Design, Selection, Coordination, Use, Understanding, Information, Other
"""

import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up plotting style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)


def categorize_barrier(barrier_text):
    """
    Map specific barrier descriptions to standardized barrier categories.
    
    These barriers are adapted from Ko et al. (2004) learning barrier framework,
    with "computer" changed to "robot" for this study.
    
    Standard categories:
    - Design: I don't know what I want the robot to do...
    - Selection: I think I know what I want the robot to do, but I don't know what to use...
    - Coordination: I think I know what things to use, but I don't know how to make them work together...
    - Use: I think I know what to use, but I don't know how to use it...
    - Understanding: I thought I knew how to use this, but it didn't do what I expected...
    - Information: I think I know why it didn't do what I expected, but I don't know how to check...
    - Other: Any barrier text that doesn't match the above categories
    """
    if not barrier_text or pd.isna(barrier_text):
        return 'Other'
    
    # Normalize: lowercase, strip whitespace, and normalize apostrophes
    # Data uses curly apostrophes (U+2019 ') not straight apostrophes (U+0027 ')
    normalized = barrier_text.lower().strip()
    # Replace curly apostrophes (both U+2018 and U+2019) with straight ones for easier matching
    normalized = normalized.replace('\u2019', "'").replace('\u2018', "'")
    
    # Exact matching with the actual barrier texts used in the study
    # After apostrophe normalization, we can use straight apostrophes in patterns
    
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


def load_interaction_data(data_dir):
    """
    Load all participant interaction data from the data directory.
    
    For each request:
    - 'category' = the learning barrier they reported when starting the session
    - 'most_useful_category' = the resource type (Chat/Read/Watch) they found most useful
    
    Returns:
        DataFrame with request-level data mapping barriers to useful resources
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
            
            # The learning barrier category they selected when starting the request
            initial_category = request_data.get('category', 'Unknown')
            
            # The resource type they found most useful (from feedback when closing)
            feedback = request_data.get('feedback', [])
            if feedback and len(feedback) > 0:
                most_useful_resource_type = feedback[0].get('most_useful_category', None)
                satisfaction = feedback[0].get('rate_satisfaction', None)
                was_category_correct = feedback[0].get('was_category_correct', None)
                
                # Use the corrected category if participant said initial was incorrect
                if was_category_correct == "No" and 'category' in feedback[0]:
                    learning_barrier = feedback[0]['category']
                else:
                    learning_barrier = initial_category
            else:
                most_useful_resource_type = None
                satisfaction = None
                was_category_correct = None
                learning_barrier = initial_category
            
            request_data_list.append({
                'participant_id': participant_id,
                'request_id': request_data.get('request_id', ''),
                'initial_category': initial_category,
                'learning_barrier': learning_barrier,
                'most_useful_resource_type': most_useful_resource_type,
                'satisfaction': satisfaction,
                'was_category_correct': was_category_correct,
                'description': request_data.get('description', ''),
                'created_at': request_data.get('created_at', ''),
                'closed_at': request_data.get('closed_at', '')
            })
    
    df = pd.DataFrame(request_data_list)
    
    # Add standardized barrier category
    df['barrier_category'] = df['learning_barrier'].apply(categorize_barrier)
    
    return df


def analyze_barrier_to_resource_relationship(df):
    """
    Answer the question: What type of resource did participants find most useful 
    for each learning barrier category?
    
    This cross-tabulates:
    - Learning Barrier Category (standardized into 7 categories)
    - Most Useful Resource Type (reported when closing the request)
    """
    print("=" * 80)
    print("RESEARCH QUESTION:")
    print("What type of learning material does a person prefer based on the")
    print("type of learning barrier they are facing?")
    print("=" * 80)
    print()
    print("NOTE: Barriers are grouped into standardized categories:")
    print("  - Design: Don't know what I want to do")
    print("  - Selection: Know what to do, don't know what to use")
    print("  - Coordination: Know what to use, don't know how to combine them")
    print("  - Use: Know what to use, don't know how to use it")
    print("  - Understanding: Thought I knew, but it didn't work as expected")
    print("  - Information: Know why it failed, don't know how to check")
    print("  - Other: Everything else")
    print("=" * 80)
    print()
    
    # Filter to requests where participant provided feedback
    df_with_feedback = df[df['most_useful_resource_type'].notna()].copy()
    
    print(f"Total requests analyzed: {len(df)}")
    print(f"Requests with feedback (most useful resource reported): {len(df_with_feedback)}")
    print(f"Unique participants: {df['participant_id'].nunique()}")
    print()
    
    # Define order for barrier categories (from Ko et al. framework)
    category_order = ['Design', 'Selection', 'Coordination', 'Use', 'Understanding', 'Information', 'Other']
    
    # Main cross-tabulation: Learning Barrier Category -> Most Useful Resource
    print("=" * 80)
    print("CROSS-TABULATION: Barrier Category → Most Useful Resource Type")
    print("=" * 80)
    print()
    
    crosstab = pd.crosstab(
        df_with_feedback['barrier_category'], 
        df_with_feedback['most_useful_resource_type'],
        margins=True
    )
    # Reorder rows to match framework order (keep 'All' row at bottom)
    row_order = [cat for cat in category_order if cat in crosstab.index and cat != 'All'] + ['All']
    crosstab = crosstab.reindex(row_order)
    print(crosstab)
    print()
    
    # Percentage breakdown (shows % for each resource type within each barrier)
    print("=" * 80)
    print("PERCENTAGE BREAKDOWN: What % Found Each Resource Most Useful")
    print("(Rows sum to 100%)")
    print("=" * 80)
    print()
    
    crosstab_pct = pd.crosstab(
        df_with_feedback['barrier_category'], 
        df_with_feedback['most_useful_resource_type'],
        normalize='index'
    ) * 100
    # Reorder rows to match framework order
    crosstab_pct = crosstab_pct.reindex([cat for cat in category_order if cat in crosstab_pct.index])
    print(crosstab_pct.round(1))
    print()
    
    # Summary for each barrier category
    print("=" * 80)
    print("SUMMARY: Most Useful Resource for Each Barrier Category")
    print("=" * 80)
    print()
    
    barrier_summary = []
    
    # Use the same category order as defined above
    for barrier in category_order:
        barrier_data = df_with_feedback[df_with_feedback['barrier_category'] == barrier]
        
        if len(barrier_data) == 0:
            continue
            
        resource_counts = barrier_data['most_useful_resource_type'].value_counts()
        
        if len(resource_counts) > 0:
            most_useful = resource_counts.index[0]
            count = resource_counts.iloc[0]
            total = len(barrier_data)
            percentage = (count / total) * 100
            
            # Get distribution
            distribution = {k: v for k, v in resource_counts.items()}
            
            print(f"\n{barrier}")
            print(f"  Sample size: {total} requests")
            print(f"  Most useful: {most_useful} ({count}/{total} = {percentage:.1f}%)")
            print(f"  Distribution: {distribution}")
            
            barrier_summary.append({
                'Barrier Category': barrier,
                'Sample Size': total,
                'Most Useful Resource': most_useful,
                'Percentage': f"{percentage:.1f}%",
                'Count': f"{count}/{total}"
            })
    
    print()
    
    # Create summary table
    summary_df = pd.DataFrame(barrier_summary)
    
    print("=" * 80)
    print("QUICK REFERENCE TABLE")
    print("=" * 80)
    print()
    print(summary_df.to_string(index=False))
    print()
    
    return crosstab, crosstab_pct, summary_df


def analyze_satisfaction_by_barrier(df):
    """
    Additional analysis: Satisfaction levels for each barrier category.
    """
    print("=" * 80)
    print("ADDITIONAL ANALYSIS: Satisfaction by Barrier Category")
    print("=" * 80)
    print()
    
    df_with_satisfaction = df[df['satisfaction'].notna()].copy()
    
    if len(df_with_satisfaction) == 0:
        print("No satisfaction data available.")
        return
    
    satisfaction_crosstab = pd.crosstab(
        df_with_satisfaction['barrier_category'],
        df_with_satisfaction['satisfaction'],
        margins=True
    )
    
    print("Satisfaction levels by barrier category:")
    print(satisfaction_crosstab)
    print()
    
    # Percentage breakdown
    satisfaction_pct = pd.crosstab(
        df_with_satisfaction['barrier_category'],
        df_with_satisfaction['satisfaction'],
        normalize='index'
    ) * 100
    
    print("Percentage breakdown:")
    print(satisfaction_pct.round(1))
    print()


def analyze_category_corrections(df):
    """
    Analyze how often participants corrected their initial barrier categorization.
    """
    print("=" * 80)
    print("DEEPER ANALYSIS 1: Category Self-Correction Patterns")
    print("=" * 80)
    print()
    
    df_with_feedback = df[df['was_category_correct'].notna()].copy()
    
    correction_counts = df_with_feedback['was_category_correct'].value_counts()
    total = len(df_with_feedback)
    
    print(f"Total requests with category validation: {total}")
    for answer, count in correction_counts.items():
        pct = (count / total) * 100
        print(f"  {answer}: {count} ({pct:.1f}%)")
    print()
    
    # Which initial categories were most often corrected?
    corrections = df_with_feedback[df_with_feedback['was_category_correct'] == 'No']
    
    if len(corrections) > 0:
        print(f"Category corrections made: {len(corrections)} requests")
        print("\nWhich initial categories were corrected:")
        initial_corrected = corrections['initial_category'].value_counts()
        for cat, count in initial_corrected.items():
            print(f"  '{cat}': {count} times")
        
        print("\nWhat they were corrected to:")
        corrected_to = corrections['learning_barrier'].value_counts()
        for cat, count in corrected_to.items():
            print(f"  '{cat}': {count} times")
        print()


def analyze_participant_patterns(df):
    """
    Analyze patterns at the participant level.
    """
    print("=" * 80)
    print("DEEPER ANALYSIS 2: Participant-Level Patterns")
    print("=" * 80)
    print()
    
    # Participants with multiple requests
    request_counts = df.groupby('participant_id').size().sort_values(ascending=False)
    multi_request = request_counts[request_counts > 1]
    
    print(f"Total participants: {len(request_counts)}")
    print(f"Participants with multiple requests: {len(multi_request)}")
    print(f"Average requests per participant: {request_counts.mean():.2f}")
    print()
    
    if len(multi_request) > 0:
        print("Top participants by number of requests:")
        for pid, count in multi_request.head(10).items():
            print(f"  {pid}: {count} requests")
        print()
        
        # Do participants stick to one resource type?
        print("Resource preference consistency (participants with 2+ requests):")
        for pid in multi_request.index[:5]:
            participant_data = df[df['participant_id'] == pid]
            resources = participant_data['most_useful_resource_type'].dropna()
            if len(resources) > 0:
                unique_resources = resources.nunique()
                most_common = resources.mode().iloc[0] if len(resources) > 0 else 'N/A'
                print(f"  {pid}: Used {unique_resources} different resource types, preferred {most_common}")
        print()


def analyze_satisfaction_resource_match(df):
    """
    Analyze if certain resource-barrier combinations lead to higher satisfaction.
    """
    print("=" * 80)
    print("DEEPER ANALYSIS 3: Satisfaction by Resource-Barrier Match")
    print("=" * 80)
    print()
    
    df_complete = df[(df['most_useful_resource_type'].notna()) & 
                     (df['satisfaction'].notna())].copy()
    
    # Overall satisfaction by resource type
    print("Average satisfaction by resource type:")
    satisfaction_map = {'Very Satisfied': 5, 'Satisfied': 4, 'Neutral': 3, 
                       'Dissatisfied': 2, 'Very Dissatisfied': 1}
    df_complete['satisfaction_score'] = df_complete['satisfaction'].map(satisfaction_map)
    
    resource_satisfaction = df_complete.groupby('most_useful_resource_type')['satisfaction_score'].agg(['mean', 'count'])
    for resource, row in resource_satisfaction.iterrows():
        print(f"  {resource}: {row['mean']:.2f}/5.0 (n={int(row['count'])})")
    print()
    
    # Which barrier-resource combinations are most satisfying?
    print("Most satisfying barrier-resource combinations (satisfaction >= 4.0):")
    combo_satisfaction = df_complete.groupby(['barrier_category', 'most_useful_resource_type'])['satisfaction_score'].agg(['mean', 'count'])
    combo_satisfaction = combo_satisfaction[combo_satisfaction['count'] >= 2]  # At least 2 samples
    top_combos = combo_satisfaction[combo_satisfaction['mean'] >= 4.0].sort_values('mean', ascending=False)
    
    for (barrier, resource), row in top_combos.head(10).iterrows():
        print(f"  {barrier} + {resource}: {row['mean']:.2f}/5.0 (n={int(row['count'])})")
    print()


def analyze_none_patterns(df):
    """
    Analyze cases where participants said 'None' was most useful.
    """
    print("=" * 80)
    print("DEEPER ANALYSIS 4: When No Resource Was Helpful")
    print("=" * 80)
    print()
    
    none_cases = df[df['most_useful_resource_type'] == 'None'].copy()
    
    print(f"Requests where 'None' was most useful: {len(none_cases)}")
    
    if len(none_cases) > 0:
        print("\nBarrier categories where no resource was helpful:")
        barrier_counts = none_cases['barrier_category'].value_counts()
        for barrier, count in barrier_counts.items():
            print(f"  {barrier}: {count}")
        
        print("\nSatisfaction levels when no resource helped:")
        if 'satisfaction' in none_cases.columns:
            satisfaction_counts = none_cases['satisfaction'].value_counts()
            for sat, count in satisfaction_counts.items():
                print(f"  {sat}: {count}")
        print()


def analyze_barrier_frequency(df):
    """
    Analyze which barrier categories are most common and their outcomes.
    """
    print("=" * 80)
    print("DEEPER ANALYSIS 5: Barrier Category Frequency and Outcomes")
    print("=" * 80)
    print()
    
    barrier_counts = df['barrier_category'].value_counts()
    
    print("Most common barrier categories:")
    for barrier, count in barrier_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {count:2d} ({pct:5.1f}%): {barrier}")
    print()
    
    # Success rate by barrier (using satisfaction as proxy)
    df_with_sat = df[df['satisfaction'].notna()].copy()
    satisfaction_map = {'Very Satisfied': 1, 'Satisfied': 1, 'Neutral': 0, 
                       'Dissatisfied': 0, 'Very Dissatisfied': 0}
    df_with_sat['success'] = df_with_sat['satisfaction'].map(satisfaction_map)
    
    barrier_success = df_with_sat.groupby('barrier_category').agg({
        'success': ['mean', 'count']
    }).round(3)
    barrier_success.columns = ['success_rate', 'count']
    barrier_success = barrier_success[barrier_success['count'] >= 2].sort_values('success_rate', ascending=False)
    
    print("Barrier categories with highest success rate (Satisfied/Very Satisfied):")
    for barrier, row in barrier_success.iterrows():
        print(f"  {row['success_rate']*100:.1f}% ({int(row['count'])}): {barrier}")
    print()


def create_visualizations(df, output_dir='./'):
    """
    Create visualizations showing the relationship between barrier categories 
    and most useful resource types.
    """
    print("=" * 80)
    print("Creating Visualizations...")
    print("=" * 80)
    print()
    
    # Prepare data - only use requests with feedback
    df_with_feedback = df[df['most_useful_resource_type'].notna()].copy()
    
    if len(df_with_feedback) == 0:
        print("No feedback data available for visualization.")
        return
    
    # Define category order
    category_order = ['Design', 'Selection', 'Coordination', 'Use', 'Understanding', 'Information', 'Other']
    
    # 1. Heatmap: Barrier Category → Most Useful Resource
    fig, ax = plt.subplots(figsize=(10, 8))
    
    crosstab = pd.crosstab(
        df_with_feedback['barrier_category'], 
        df_with_feedback['most_useful_resource_type']
    )
    
    # Reorder rows
    crosstab = crosstab.reindex([cat for cat in category_order if cat in crosstab.index])
    
    sns.heatmap(crosstab, annot=True, fmt='d', cmap='Blues', ax=ax, cbar_kws={'label': 'Number of Requests'})
    plt.title('Barrier Category → Most Useful Resource Type\n(Number of Requests)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Most Useful Resource Type', fontsize=11)
    plt.ylabel('Barrier Category (Standardized)', fontsize=11)
    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    heatmap_path = os.path.join(output_dir, 'barrier_to_resource_heatmap.png')
    plt.savefig(heatmap_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {heatmap_path}")
    plt.close()
    
    # 2. Stacked bar chart (percentage)
    fig, ax = plt.subplots(figsize=(12, 8))
    
    crosstab_pct = pd.crosstab(
        df_with_feedback['barrier_category'], 
        df_with_feedback['most_useful_resource_type'],
        normalize='index'
    ) * 100
    
    # Order by standard category order
    crosstab_pct = crosstab_pct.reindex([cat for cat in category_order if cat in crosstab_pct.index])
    
    crosstab_pct.plot(kind='barh', stacked=True, ax=ax, 
                      color=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'])
    plt.title('Most Useful Resource Type by Barrier Category\n(Percentage Distribution)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Percentage of Participants', fontsize=11)
    plt.ylabel('Barrier Category (Standardized)', fontsize=11)
    plt.legend(title='Most Useful\nResource Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xlim(0, 100)
    
    # Add percentage labels
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f%%', label_type='center', fontsize=8)
    
    plt.tight_layout()
    
    stacked_bar_path = os.path.join(output_dir, 'barrier_to_resource_stacked.png')
    plt.savefig(stacked_bar_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {stacked_bar_path}")
    plt.close()
    
    # 3. Grouped bar chart (counts)
    fig, ax = plt.subplots(figsize=(12, 8))
    
    crosstab.plot(kind='barh', ax=ax, 
                  color=['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'])
    plt.title('Most Useful Resource Type by Barrier Category\n(Number of Requests)', 
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Number of Requests', fontsize=11)
    plt.ylabel('Barrier Category (Standardized)', fontsize=11)
    plt.legend(title='Most Useful\nResource Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    grouped_bar_path = os.path.join(output_dir, 'barrier_to_resource_grouped.png')
    plt.savefig(grouped_bar_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {grouped_bar_path}")
    plt.close()
    
    print()


def main():
    """
    Main analysis function.
    
    Research Question: What type of learning material does a person prefer 
    based on the type of learning barrier they are facing?
    """
    # Get the script directory and find the data folder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    data_dir = os.path.join(repo_root, "data")
    
    print("\n")
    print("=" * 80)
    print("BARRIER → RESOURCE ANALYSIS (with Standardized Categories)")
    print("=" * 80)
    print("Loading interaction data from:", data_dir)
    print()
    
    df = load_interaction_data(data_dir)
    
    if df is None or len(df) == 0:
        print("Error: No data loaded. Please check the data directory.")
        return
    
    print(f"✓ Loaded {len(df)} requests from {df['participant_id'].nunique()} participants")
    print()
    
    # Main analysis: Learning Barrier Category → Most Useful Resource
    crosstab, crosstab_pct, summary_df = analyze_barrier_to_resource_relationship(df)
    
    # Additional analysis
    analyze_satisfaction_by_barrier(df)
    
    # DEEPER ANALYSES - Uncovering hidden patterns
    analyze_category_corrections(df)
    analyze_participant_patterns(df)
    analyze_satisfaction_resource_match(df)
    analyze_none_patterns(df)
    analyze_barrier_frequency(df)
    
    # Create visualizations
    output_dir = os.path.join(repo_root, "images")
    os.makedirs(output_dir, exist_ok=True)
    create_visualizations(df, output_dir)
    
    # Save detailed data to CSV for further analysis
    output_csv = os.path.join(repo_root, "data", "barrier_to_resource_analysis.csv")
    df.to_csv(output_csv, index=False)
    print(f"✓ Saved detailed data to: {output_csv}")
    print()
    
    # Save summary table
    summary_csv = os.path.join(repo_root, "data", "barrier_resource_summary.csv")
    summary_df.to_csv(summary_csv, index=False)
    print(f"✓ Saved summary table to: {summary_csv}")
    print()
    
    print("=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nKey outputs:")
    print(f"  1. Visualizations: {output_dir}/")
    print(f"  2. Detailed data: {output_csv}")
    print(f"  3. Summary table: {summary_csv}")
    print()


if __name__ == "__main__":
    main()
