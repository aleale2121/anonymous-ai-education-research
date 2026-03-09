import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_topic_proportions(input_path: str, output_path: str):

    df = pd.read_csv(input_path)

    # Use Topic Category as index
    df = df.set_index("Topic Category")

    df_t = df.T

    # Convert to percentages
    df_percent = df_t.div(df_t.sum(axis=1), axis=0) * 100

    # Sort categories alphabetically
    df_percent = df_percent.reindex(sorted(df_percent.columns), axis=1)

    # Generate colors
    colors = (
        sns.color_palette("hls")
        + sns.color_palette("Dark2")
        + sns.color_palette("tab20")
    )
    colors = colors[:df_percent.shape[1]]

    color_map = dict(zip(df_percent.columns, colors))

    plt.figure(figsize=(32, 16))

    ax = df_percent.plot(
        kind="bar",
        stacked=True,
        width=0.80,
        color=[color_map[col] for col in df_percent.columns]
    )

    # Tick formatting
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)

    for label in ax.get_xticklabels():
        label.set_fontweight('bold')

    for label in ax.get_yticklabels():
        label.set_fontweight('bold')

    # Add percentage labels
    for container in ax.containers:
        labels = [f"{v:.1f}%" if v > 0.9 else "" for v in container.datavalues]
        texts = ax.bar_label(
            container,
            labels=labels,
            label_type="center",
            fontsize=20,
            color="black"
        )
        for t in texts:
            t.set_fontweight("bold")

    plt.title(
        "AI in Education Global Topics Percentage Distribution by Year",
        fontsize=24,
        fontweight="bold"
    )

    plt.xlabel("Year", fontsize=22, fontweight="bold")
    plt.ylabel("Proportion of Yearly Discussion (%)", fontsize=22, fontweight="bold")

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=color_map[col])
        for col in df_percent.columns
    ]

    plt.subplots_adjust(left=0.04, right=0.62)

    legend = plt.legend(
        handles[::-1],
        df_percent.columns,
        title="Topic Categories",
        loc="upper center",
        bbox_to_anchor=(1.32, 1.0),
        ncol=1,
        frameon=False,
        fontsize=24,
        title_fontsize=26,
        labelspacing=1.4,
        handletextpad=0.8,
        borderpad=1.4
    )

    legend.get_title().set_fontweight("bold")

    for text in legend.get_texts():
        text.set_fontweight("bold")

    plt.savefig(output_path)
    plt.close()

    print(f"Saved figure → {output_path}")