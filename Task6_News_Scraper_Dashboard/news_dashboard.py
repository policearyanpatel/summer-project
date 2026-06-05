import customtkinter as ctk
import feedparser
import json
import csv

from tkinter import filedialog
from datetime import datetime
from collections import Counter

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class NewsDashboard:

    def __init__(self, root):

        self.root = root
        self.root.title("News Intelligence Dashboard Pro")

        try:
            self.root.state("zoomed")
        except:
            self.root.geometry("1400x850")

        self.root.configure(fg_color="#F5F5F5")

        self.news_data = []
        self.dark_mode = False

        self.build_ui()

    def build_ui(self):

        # ==========================
        # HEADER
        # ==========================

        self.title_label = ctk.CTkLabel(
            self.root,
            text="NEWS INTELLIGENCE DASHBOARD PRO",
            font=("Segoe UI", 30, "bold"),
            text_color="#111827"
        )

        self.title_label.pack(pady=(15, 5))

        self.subtitle = ctk.CTkLabel(
            self.root,
            text="Multi Source News Analytics Platform",
            font=("Segoe UI", 15),
            text_color="#6B7280"
        )

        self.subtitle.pack()

        # ==========================
        # DASHBOARD CARDS
        # ==========================

        self.cards_frame = ctk.CTkFrame(
            self.root,
            fg_color="#F5F5F5"
        )

        self.cards_frame.pack(
            fill="x",
            padx=20,
            pady=15
        )

        self.total_card = ctk.CTkFrame(
            self.cards_frame,
            width=250,
            height=110,
            fg_color="#FFFFFF"
        )

        self.total_card.pack(
            side="left",
            padx=10
        )

        self.total_title = ctk.CTkLabel(
            self.total_card,
            text="Total Headlines",
            font=("Segoe UI", 18, "bold")
        )

        self.total_title.pack(pady=(20, 5))

        self.total_value = ctk.CTkLabel(
            self.total_card,
            text="0",
            font=("Segoe UI", 26, "bold")
        )

        self.total_value.pack()

        # Source Card

        self.source_card = ctk.CTkFrame(
            self.cards_frame,
            width=250,
            height=110,
            fg_color="#FFFFFF"
        )

        self.source_card.pack(
            side="left",
            padx=10
        )
        self.analytics_card = ctk.CTkFrame(
            self.cards_frame,
            width=350,
            height=110,
            fg_color="#FFFFFF"
        )

        self.analytics_card.pack(
            side="left",
            padx=10
        )

        ctk.CTkLabel(
            self.analytics_card,
            text="Trending Keyword",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(20,5))

        self.keyword_value = ctk.CTkLabel(
            self.analytics_card,
            text="N/A",
            font=("Segoe UI", 22, "bold")
        )

        self.keyword_value.pack()

        ctk.CTkLabel(
            self.source_card,
            text="Sources Loaded",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(20, 5))

        self.source_value = ctk.CTkLabel(
            self.source_card,
            text="3",
            font=("Segoe UI", 26, "bold")
        )

        self.source_value.pack()

        # Updated Card

        self.time_card = ctk.CTkFrame(
            self.cards_frame,
            width=350,
            height=110,
            fg_color="#FFFFFF"
        )

        self.time_card.pack(
            side="left",
            padx=10
        )

        ctk.CTkLabel(
            self.time_card,
            text="Last Updated",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=(20, 5))

        self.time_value = ctk.CTkLabel(
            self.time_card,
            text="Not Loaded",
            font=("Segoe UI", 16)
        )

        self.time_value.pack()

        # ==========================
        # SEARCH BAR
        # ==========================

        self.search_entry = ctk.CTkEntry(
            self.root,
            placeholder_text="Search News..."
        )

        self.search_entry.pack(
            fill="x",
            padx=25,
            pady=10
        )

        # ==========================
        # NEWS PANEL
        # ==========================

        self.news_box = ctk.CTkTextbox(
            self.root,
            height=200
        )

        self.news_box.pack(
            fill="x",
            padx=25,
            pady=10
        )
        self.sentiment_frame = ctk.CTkFrame(
            self.root,
            fg_color="#FFFFFF"
        )

        self.sentiment_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        self.positive_label = ctk.CTkLabel(
            self.sentiment_frame,
            text="Positive : 0",
            font=("Segoe UI", 16, "bold")
        )

        self.positive_label.pack(
            side="left",
            padx=20,
            pady=10
        )

        self.neutral_label = ctk.CTkLabel(
            self.sentiment_frame,
            text="Neutral : 0",
            font=("Segoe UI", 16, "bold")
        )

        self.neutral_label.pack(
            side="left",
            padx=20
        )

        self.negative_label = ctk.CTkLabel(
            self.sentiment_frame,
            text="Negative : 0",
            font=("Segoe UI", 16, "bold")
        )

        self.negative_label.pack(
            side="left",
            padx=20
        )
        self.keyword_frame = ctk.CTkFrame(
            self.root,
            fg_color="#FFFFFF"
        )

        self.keyword_frame.pack(
            fill="x",
            padx=25,
            pady=10
        )

        ctk.CTkLabel(
            self.keyword_frame,
            text="Top Keywords",
            font=("Segoe UI",18,"bold")
        ).pack(pady=10)

        self.keyword_box = ctk.CTkTextbox(
            self.keyword_frame,
            height=70
        )

        self.keyword_box.pack(
            fill="x",
            padx=15,
            pady=10
        )
        # ==========================
        # BUTTONS
        # ==========================

        self.button_frame = ctk.CTkFrame(
            self.root,
            fg_color="#F5F5F5"
        )

        self.button_frame.pack(
            pady=10,
            before=self.news_box
        )

        self.fetch_btn = ctk.CTkButton(
            self.button_frame,
            text="Fetch News",
            command=self.fetch_news
        )

        self.fetch_btn.pack(
            side="left",
            padx=10
        )
        self.search_btn = ctk.CTkButton(
            self.button_frame,
            text="Search News",
            command=self.search_news
        )

        self.search_btn.pack(
            side="left",
            padx=10
        )

        self.export_txt_btn = ctk.CTkButton(
            self.button_frame,
            text="Export TXT",
            command=self.export_txt
        )

        self.export_txt_btn.pack(
            side="left",
            padx=10
        )

        self.export_csv_btn = ctk.CTkButton(
            self.button_frame,
            text="Export CSV",
            command=self.export_csv
        )

        self.export_csv_btn.pack(
            side="left",
            padx=10
        )

        self.theme_btn = ctk.CTkButton(
            self.button_frame,
            text="Dark Mode",
            command=self.toggle_theme
        )

        self.theme_btn.pack(
            side="left",
            padx=10
        )
    def fetch_news(self):

        self.news_box.delete("1.0", "end")

        feeds = [

            ("BBC", "https://feeds.bbci.co.uk/news/rss.xml"),

            ("Reuters",
             "https://feeds.reuters.com/reuters/topNews"),

            ("Google News",
             "https://news.google.com/rss")
        ]

        self.news_data.clear()

        for source, url in feeds:

            try:

                feed = feedparser.parse(url)

                for entry in feed.entries[:15]:

                    headline = entry.title

                    self.news_data.append({
                        "source": source,
                        "headline": headline
                    })

            except:

                pass

        for item in self.news_data:

            self.news_box.insert(
                "end",
                f"[{item['source']}]\n"
                f"{item['headline']}\n\n"
            )

        self.total_value.configure(
            text=str(len(self.news_data))
        )

        self.time_value.configure(
            text=datetime.now().strftime(
                "%d-%m-%Y %I:%M %p"
            )
        )
        self.update_analytics()
        with open(
            "news_data.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.news_data,
                file,
                indent=4,
                ensure_ascii=False
            )
    def search_news(self):

        keyword = self.search_entry.get().lower()

        self.news_box.delete("1.0", "end")

        for item in self.news_data:

            if keyword in item["headline"].lower():

                self.news_box.insert(
                    "end",
                    f"[{item['source']}]\n"
                    f"{item['headline']}\n\n"
                )

    def export_txt(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".txt"
        )

        if not path:
            return

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as file:

            for item in self.news_data:

                file.write(
                    f"[{item['source']}] "
                    f"{item['headline']}\n"
                )

    def export_csv(self):

        path = filedialog.asksaveasfilename(
            defaultextension=".csv"
        )

        if not path:
            return

        with open(
            path,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "Source",
                "Headline"
            ])

            for item in self.news_data:

                writer.writerow([
                    item["source"],
                    item["headline"]
                ])

    def toggle_theme(self):

        if self.dark_mode:

            ctk.set_appearance_mode("light")

            self.theme_btn.configure(
                text="Dark Mode"
            )

            self.dark_mode = False

        else:

            ctk.set_appearance_mode("dark")

            self.theme_btn.configure(
                text="Light Mode"
            )

            self.dark_mode = True

    def update_analytics(self):

        words = []

        positive = 0
        neutral = 0
        negative = 0

        positive_words = [
            "growth",
            "success",
            "win",
            "profit",
            "rise",
            "good",
            "positive"
        ]

        negative_words = [
            "crash",
            "loss",
            "war",
            "attack",
            "fall",
            "negative",
            "decline"
        ]

        for item in self.news_data:

            headline = item["headline"].lower()

            words.extend(
                headline.split()
            )

            if any(
                word in headline
                for word in positive_words
            ):
                positive += 1

            elif any(
                word in headline
                for word in negative_words
            ):
                negative += 1

            else:
                neutral += 1

        common_words = Counter(words)

        stop_words = {
            "the",
            "and",
            "of",
            "to",
            "in",
            "for",
            "on",
            "with",
            "a"
        }

        filtered = {
            k: v
            for k, v in common_words.items()
            if k not in stop_words
            and len(k) > 3
        }

        if filtered:

            keyword = max(
                filtered,
                key=filtered.get
            )

            self.keyword_value.configure(
                text=keyword.title()
            )

            self.keyword_box.delete(
                "1.0",
                "end"
            )

            top_keywords = sorted(
                filtered.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]

            for word, count in top_keywords:

                self.keyword_box.insert(
                    "end",
                    f"{word.title()} ({count})\n"
                )
        self.positive_label.configure(
            text=f"Positive : {positive}"
        )

        self.neutral_label.configure(
            text=f"Neutral : {neutral}"
        )

        self.negative_label.configure(
            text=f"Negative : {negative}"
        )
if __name__ == "__main__":

    root = ctk.CTk()

    app = NewsDashboard(root)

    root.mainloop()