import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from signals import SIGNALS, compute_signal, get_signals_by_category

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SignalVisualizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sinyaller ve Sistemler — Sinyal Görselleştirici")
        self.geometry("1120x680")
        self.minsize(920, 560)

        self.active_category = "basic"
        self.selected_signal = get_signals_by_category("basic")[0]
        self.signal_buttons: dict[str, ctk.CTkButton] = {}

        self._build_layout()
        self._populate_signal_list()
        self._select_signal(self.selected_signal)

    def _build_layout(self):
        self.grid_columnconfigure(0, weight=0, minsize=300)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SOL PANEL ---
        left_panel = ctk.CTkFrame(self, width=300, corner_radius=0)
        left_panel.grid(row=0, column=0, sticky="nsew")
        left_panel.grid_rowconfigure(2, weight=1)

        title_lbl = ctk.CTkLabel(
            left_panel,
            text="Sinyal Kütüphanesi (20)",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        )
        title_lbl.grid(row=0, column=0, padx=16, pady=(16, 10), sticky="ew")

        # Kategori Segmented Butonu
        self.category_seg = ctk.CTkSegmentedButton(
            left_panel,
            values=["Temel (10)", "Diğer (10)"],
            command=self._on_category_change,
        )
        self.category_seg.set("Temel (10)")
        self.category_seg.grid(row=1, column=0, padx=16, pady=(0, 10), sticky="ew")

        # Sinyal Listesi
        self.list_frame = ctk.CTkScrollableFrame(left_panel, corner_radius=8)
        self.list_frame.grid(row=2, column=0, padx=16, pady=(0, 12), sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        # Parametre Kontrolleri (2 Sabit Slider + Sıfırla)
        ctrl_frame = ctk.CTkFrame(left_panel, corner_radius=8)
        ctrl_frame.grid(row=3, column=0, padx=16, pady=(0, 16), sticky="ew")
        ctrl_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            ctrl_frame,
            text="Parametreler",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, padx=12, pady=(10, 4), sticky="ew")

        self.amp_label = ctk.CTkLabel(
            ctrl_frame, text="Genlik (A): 1.00", anchor="w", font=ctk.CTkFont(size=12)
        )
        self.amp_label.grid(row=1, column=0, padx=12, pady=(2, 0), sticky="ew")

        self.amp_slider = ctk.CTkSlider(
            ctrl_frame, from_=0.2, to=5.0, number_of_steps=48, command=self._on_param_change
        )
        self.amp_slider.set(1.0)
        self.amp_slider.grid(row=2, column=0, padx=12, pady=(2, 8), sticky="ew")

        self.freq_label = ctk.CTkLabel(
            ctrl_frame, text="Frekans / Ölçek (f): 1.00", anchor="w", font=ctk.CTkFont(size=12)
        )
        self.freq_label.grid(row=3, column=0, padx=12, pady=(2, 0), sticky="ew")

        self.freq_slider = ctk.CTkSlider(
            ctrl_frame, from_=0.1, to=3.0, number_of_steps=29, command=self._on_param_change
        )
        self.freq_slider.set(1.0)
        self.freq_slider.grid(row=4, column=0, padx=12, pady=(2, 10), sticky="ew")

        reset_btn = ctk.CTkButton(
            ctrl_frame,
            text="Varsayılana Sıfırla",
            height=30,
            fg_color="transparent",
            border_width=1,
            command=self._reset_params,
        )
        reset_btn.grid(row=5, column=0, padx=12, pady=(0, 12), sticky="ew")

        # --- SAĞ PANEL (GRAFIK ALANI) ---
        right_panel = ctk.CTkFrame(self, corner_radius=0, fg_color="#141820")
        right_panel.grid(row=0, column=1, sticky="nsew")
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)

        header_frame = ctk.CTkFrame(right_panel, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(16, 4), sticky="ew")
        header_frame.grid_columnconfigure(0, weight=1)

        self.signal_title_lbl = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(size=18, weight="bold"),
            anchor="w",
        )
        self.signal_title_lbl.grid(row=0, column=0, sticky="w")

        self.formula_lbl = ctk.CTkLabel(
            header_frame,
            text="",
            font=ctk.CTkFont(family="Menlo", size=13),
            text_color="#7dd3fc",
            anchor="w",
        )
        self.formula_lbl.grid(row=1, column=0, pady=(2, 0), sticky="w")

        # Matplotlib Figürü
        plt.style.use("dark_background")
        self.fig, self.ax = plt.subplots(figsize=(7.5, 4.6), dpi=100)
        self.fig.patch.set_facecolor("#141820")
        self.ax.set_facecolor("#1b212c")

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=8, sticky="nsew")

        # Alt Bilgi Satırı
        self.footer_lbl = ctk.CTkLabel(
            right_panel,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="#9ca3af",
            anchor="w",
        )
        self.footer_lbl.grid(row=2, column=0, padx=20, pady=(0, 14), sticky="ew")

    def _on_category_change(self, value: str):
        self.active_category = "basic" if value.startswith("Temel") else "other"
        self._populate_signal_list()
        signals_in_cat = get_signals_by_category(self.active_category)
        if self.selected_signal not in signals_in_cat and signals_in_cat:
            self._select_signal(signals_in_cat[0])
        else:
            self._highlight_selected_button()

    def _populate_signal_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        self.signal_buttons.clear()

        for idx, name in enumerate(get_signals_by_category(self.active_category), start=1):
            btn = ctk.CTkButton(
                self.list_frame,
                text=f"{idx}. {name}",
                anchor="w",
                height=32,
                fg_color="transparent",
                text_color="#e5e7eb",
                hover_color="#283142",
                command=lambda s=name: self._select_signal(s),
            )
            btn.grid(row=idx - 1, column=0, pady=2, sticky="ew")
            self.signal_buttons[name] = btn

        self._highlight_selected_button()

    def _highlight_selected_button(self):
        for name, btn in self.signal_buttons.items():
            if name == self.selected_signal:
                btn.configure(fg_color="#1f6aa5", text_color="#ffffff")
            else:
                btn.configure(fg_color="transparent", text_color="#e5e7eb")

    def _select_signal(self, name: str):
        self.selected_signal = name
        self._highlight_selected_button()
        self._draw_signal()

    def _on_param_change(self, _value=None):
        self._draw_signal()

    def _reset_params(self):
        self.amp_slider.set(1.0)
        self.freq_slider.set(1.0)
        self._draw_signal()

    def _draw_signal(self):
        amp = float(self.amp_slider.get())
        freq = float(self.freq_slider.get())

        self.amp_label.configure(text=f"Genlik (A): {amp:.2f}")
        self.freq_label.configure(text=f"Frekans / Ölçek (f): {freq:.2f}")

        x, y, domain, kind, formula_str, ylim = compute_signal(self.selected_signal, amp, freq)

        self.signal_title_lbl.configure(text=self.selected_signal)
        self.formula_lbl.configure(text=f"Formül: {formula_str}")
        self.footer_lbl.configure(text=f"Tür: {kind}")

        self.ax.clear()
        self.ax.set_facecolor("#1b212c")

        if domain == "discrete":
            markerline, stemlines, baseline = self.ax.stem(x, y, linefmt="#38bdf8", markerfmt="o", basefmt="#64748b")
            markerline.set_markersize(5)
            markerline.set_markerfacecolor("#38bdf8")
            stemlines.set_linewidth(1.5)
            self.ax.set_xlabel("n (Ayrık Zaman İndisi)")
        else:
            self.ax.plot(x, y, color="#38bdf8", linewidth=2.0)
            self.ax.set_xlabel("t (Sürekli Zaman [s])")

        self.ax.set_ylim(*ylim)
        self.ax.set_ylabel("Genlik")
        self.ax.axhline(0, color="#64748b", linewidth=0.9)
        self.ax.axvline(0, color="#64748b", linewidth=0.9)
        self.ax.grid(True, linestyle="--", alpha=0.25, color="#94a3b8")
        self.ax.spines["top"].set_visible(False)
        self.ax.spines["right"].set_visible(False)
        self.ax.spines["left"].set_color("#475569")
        self.ax.spines["bottom"].set_color("#475569")

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = SignalVisualizerApp()
    app.mainloop()