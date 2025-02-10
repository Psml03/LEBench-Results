import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Define the file path
file_path = ""

# Load the Excel file
df = pd.read_excel(file_path, engine='openpyxl')

# Treat exactly 0.00% as positive
df["Degradation (%)"] = df["Degradation (%)"].apply(lambda x: 0 if abs(x) < 0.01 else x)

# Custom order for the bars
custom_order = [
    "huge write", "big write", "mid write", "small write", 
    "thr create Child", "thr create", "ref", "getpid", "cpu", "context switch",
    "big send", "send", "big recv", "recv", "select big", "select",
    "huge read", "big read", "mid read", "small read", 
    "huge page fault", "big page fault", "mid page fault", "small page fault", 
    "huge munmap", "big munmap", "mid munmap", "small munmap", 
    "huge mmap", "big mmap", "mid mmap", "small mmap", 
    "huge fork Child", "big fork Child", "fork Child", 
    "huge fork", "big fork", "fork", 
    "poll big", "poll", "epoll big", "epoll"
]


# Normalize Test Names
df["Test Name"] = df["Test Name"].str.strip().str.lower()
custom_order = [name.strip().lower() for name in custom_order]

# Size order for sorting
size_order = {"small": 1, "mid": 2, "big": 3, "huge": 4}

# Grouping functions
def group_test_names(test_name):
    match test_name.lower():
        case name if "mmap" in name: return "mmap_group"
        case name if "munmap" in name: return "munmap_group"
        case name if "page fault" in name: return "page_fault_group"
        case name if "read" in name: return "read_group"
        case name if "write" in name: return "write_group"

        case name if "big fork child" in name: return "fork_Child_group"
        case name if "huge fork child" in name: return "fork_Child_group"
        case name if "fork child" in name: return "fork_Child_group"
        case name if "huge fork" in name: return "fork_group"
        case name if "big fork" in name: return "fork_group"
        case name if "fork" in name: return "fork_group"

        case name if "thr create" in name: return "thr_create_group"
        case name if "select" in name: return "select_group"
        case name if "epoll" in name: return "epoll_group"
        case name if "poll" in name: return "poll_group"
        case name if "send" in name: return "send_group"
        case name if "recv" in name: return "recv_group"
        case name if "cpu" in name: return "cpu_group"
        case name if "ref" in name: return "ref_group"
        case name if "getpid" in name: return "getpid_group"

        case _: return "standalone_group"

#Size prefix for sorting
def extract_size_prefix(test_name):
    for size in size_order:
        if size in test_name.lower():
            return size
    return "other"

# Add grouping and sorting columns
df["Group"] = df["Test Name"].apply(group_test_names)
df["Size"] = df["Test Name"].apply(extract_size_prefix)
df["Size Order"] = df["Size"].map(size_order).fillna(0)  # Non-size tests get 0

# Map Custom Order
df["Custom Order"] = df["Test Name"].apply(
    lambda x: custom_order.index(x) if x in custom_order else len(custom_order)
)

# Sort by Custom Order, then Group, then Size Order, and finally Test Name
df.sort_values(by=["Custom Order", "Group", "Size Order", "Test Name"], inplace=True)

# Reordered Tab20 palette
palette_order = [19, 11, 17, 15, 20, 8, 7, 10, 9, 6, 5, 2, 1, 14, 13, 4, 3]
reordered_palette = [sns.color_palette("tab20")[i - 1] for i in palette_order]

# Assign colors: each group gets a distinct color
group_colors = {group: reordered_palette[i] for i, group in enumerate(df["Group"].unique())}
df["Color"] = df["Group"].map(group_colors)

# Create the vertical plot
plt.figure(figsize=(14, 24))  # Adjusted size for vertical orientation
plt.barh(df["Test Name"], df["Degradation (%)"], color=df["Color"])  # Use barh for horizontal bars

# Add labels
for index, (value, test_name) in enumerate(zip(df["Degradation (%)"], df["Test Name"])):
    label_color = "red" if value < 0 else "green"
    ha_position = 'right' if value < 0 else 'left'
    plt.text(value, index, f'{value:.2f}%', ha=ha_position, va='center',
             fontsize=16, color=label_color)

# Customize
plt.title("Performance Degradation by Test Case", fontsize=20)
plt.xlabel("Degradation (%)", fontsize=18)
plt.ylabel("Test Name", fontsize=18)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.axvline(x=0, color='black', linewidth=4)  # Baseline at 0%
plt.xlim(-8, 4)  # Start x-axis at -6
plt.xticks(ticks=range(-8, 5, 2), labels=[f"{x}%" for x in range(-8, 5, 2)], fontsize=18)  # Updated ticks
plt.yticks(fontsize=18)
plt.tight_layout()


# Save the plot to the specified path as a PNG
output_path = ""
plt.savefig(output_path, format='png', dpi=600, bbox_inches='tight')  # 600 dpi for high quality
print(f"High-resolution vertical image saved to {output_path}")

# Show the plot
plt.show()

