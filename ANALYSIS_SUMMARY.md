# Learning Resource Preference vs Learning Barrier Analysis

## Summary of Findings

This analysis examined the relationship between participants' preferred learning resources (text, video, chatbot) and the types of learning barriers they encountered while programming a robot.

### Key Findings

#### 1. **Overall Resource Preference**
- **Chat/Chatbot**: Most preferred resource (20 out of 34 requests with feedback = 58.8%)
- **Text**: Second most preferred (6 requests = 17.6%)
- **Video**: Least preferred stated resource (2 requests = 5.9%)
- **None**: 6 requests (17.6%) indicated no particular resource was most useful

#### 2. **Resource Preference by Learning Barrier Type**

| Learning Barrier | Most Preferred Resource | Preference Rate |
|-----------------|------------------------|-----------------|
| **I think I know what to use, but I don't know how to use it** | Chat | 100% (7/7) |
| **I think I know what things to use, but I don't know how to make them work together** | Chat | 60% (3/5) |
| **I thought I knew how to use this, but it didn't do what I expected** | Chat | 57.1% (4/7) |
| **I think I know what I want the robot to do, but I don't know what to use** | Chat | 50% (3/6) |
| **I don't know what I want the robot to do** | None | 66.7% (2/3) |

#### 3. **Key Insights**

**Chat is overwhelmingly preferred for technical barriers:**
- When participants know WHAT to use but not HOW to use it → 100% prefer Chat
- When participants need to integrate components → 60% prefer Chat
- When expectations don't match reality → 57.1% prefer Chat

**Conceptual barriers show different patterns:**
- When participants don't know what they want the robot to do → No clear preference (66.7% said "None" was most useful)

**Actual Usage vs Stated Preference:**
- Only 50% agreement between what users said was most useful and what they actually used most
- Users often used Video resources even when they stated Chat was most useful
- This suggests users may try multiple resource types before finding what works

### Visualizations Created

Three visualizations have been generated in the `images/` folder:

1. **barrier_preference_heatmap.png** - Shows the count of each preference type for each barrier
2. **barrier_preference_stacked_bar.png** - Shows percentage breakdown of preferences by barrier type
3. **barrier_preference_grouped_bar.png** - Shows absolute counts in a grouped format

### Data Files Created

- **data/barrier_preference_analysis.csv** - Complete dataset with all request-level data for further analysis

## Recommendations

1. **For "How to Use" barriers**: Prioritize chatbot/chat resources as they are strongly preferred
2. **For "What to Use" barriers**: Provide mixed resources (chat + video) as preferences are more distributed
3. **For conceptual barriers**: Consider that traditional resources may not be effective; users may need different intervention types

## Methodology

The analysis:
- Examined 36 requests from 20 participants
- Used feedback data to determine stated preferences ("most_useful_category")
- Counted actual usage by interaction type (chat, video, text)
- Compared stated preferences with actual usage patterns
- Created cross-tabulations and visualizations

## How to Run the Analysis

```bash
# From the repository root
python scripts/analysis.py
```

This will regenerate all statistics and visualizations.
