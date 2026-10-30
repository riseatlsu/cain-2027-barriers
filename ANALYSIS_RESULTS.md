# Learning Barrier → Most Useful Resource Analysis

## Research Question
**What type of learning material does a person prefer based on the type of learning barrier they are facing?**

## Methodology
- **Learning Barrier**: Reported by participants when they START a request (stored in `category` field)
- **Most Useful Resource**: Reported by participants when they CLOSE a request (stored in `most_useful_category` field in feedback)
- **Resource Types**: Chat, Read (text), Watch (video), or None
- **Sample**: 34 requests with feedback from 20 participants

## Key Findings

### 1. Chat is the Most Useful Resource for Technical Barriers

| Learning Barrier | Most Useful | % Choosing It | Sample Size |
|-----------------|-------------|---------------|-------------|
| **I think I know what to use, but I don't know how to use it** | Chat | 100% (7/7) | 7 |
| **I think I know what things to use, but I don't know how to make them work together** | Chat | 60% (3/5) | 5 |
| **I thought I knew how to use this, but it didn't do what I expected** | Chat | 57.1% (4/7) | 7 |
| **I think I know what I want the robot to do, but I don't know what to use** | Chat | 50% (3/6) | 6 |
| **Ending the program with input** | Chat | 100% (1/1) | 1 |
| **Multiple Choice Questions?** | Chat | 100% (1/1) | 1 |

### 2. Read (Text) is Useful for Specific Tool Questions

| Learning Barrier | Most Useful | % Choosing It | Sample Size |
|-----------------|-------------|---------------|-------------|
| **Reset robot** | Read | 100% (1/1) | 1 |
| **Wizard** | Read | 100% (1/1) | 1 |

### 3. No Clear Preference for Conceptual Barriers

| Learning Barrier | Most Useful | % Choosing It | Sample Size |
|-----------------|-------------|---------------|-------------|
| **I don't know what I want the robot to do** | None | 66.7% (2/3) | 3 |

This suggests that when participants lack conceptual understanding, the provided resources were not as helpful.

## Summary Statistics

**Overall Resource Preferences (across all barriers):**
- Chat: 20/34 requests (58.8%)
- None: 6/34 requests (17.6%)
- Read: 6/34 requests (17.6%)
- Watch: 2/34 requests (5.9%)

## Main Insights

1. **Chat/Chatbot is overwhelmingly preferred for implementation barriers**
   - When users know WHAT to use but not HOW (100% prefer Chat)
   - When users need to integrate multiple components (60% prefer Chat)
   - When debugging unexpected behavior (57.1% prefer Chat)

2. **Text resources work well for specific tool/feature questions**
   - Direct questions about specific features (Reset, Wizard) → Read preferred

3. **Conceptual barriers require different support**
   - When users don't know what they want the robot to do, most found no resource particularly helpful
   - This suggests need for alternative intervention types (e.g., examples, demonstrations)

4. **Video is rarely cited as most useful**
   - Only 2 out of 34 requests (5.9%) cited Watch/Video as most useful
   - This may warrant further investigation into video content or presentation

## Satisfaction Analysis

Overall satisfaction was high across all barrier types:
- Satisfied: 50.0% overall
- Very Satisfied: 29.4% overall
- Dissatisfied: Only 2 requests (5.9%)

The one barrier with dissatisfaction was "I don't know what I want the robot to do" (33.3% dissatisfied), reinforcing that conceptual barriers need different support approaches.

## Recommendations

1. **For implementation/how-to barriers**: Prioritize chat/interactive support
2. **For specific feature questions**: Text documentation is effective
3. **For conceptual barriers**: Consider additional resources like:
   - Worked examples
   - Interactive demonstrations
   - Goal-oriented templates
4. **For video content**: Investigate why videos are rarely cited as most useful; consider:
   - Content relevance
   - Discoverability
   - Presentation format

## Generated Files

### Visualizations (in `images/` folder)
1. `barrier_to_resource_heatmap.png` - Count matrix showing barrier → resource relationship
2. `barrier_to_resource_stacked.png` - Percentage distribution by barrier
3. `barrier_to_resource_grouped.png` - Side-by-side comparison of counts

### Data Files (in `data/` folder)
1. `barrier_to_resource_analysis.csv` - Complete request-level data
2. `barrier_resource_summary.csv` - Summary table with key statistics

## How to Reproduce

```bash
python scripts/analysis.py
```

This will regenerate all statistics, visualizations, and data files.
