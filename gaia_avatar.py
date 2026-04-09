import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPixmap, QPainter, QPen, QFont

class GaiaAvatarEngine(QWidget):
    def __init__(self, field_state, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("GAIA-TEQUMSA Companion Avatar")
        self.resize(400, 580)
        self.field_state = field_state
        self.layout = QVBoxLayout()
        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        # Timer for animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(33)  # ~30 FPS

        self.phase = 0

    def animate(self):
        # --- Unpack dynamic field variables
        rec = self.field_state.get("recognition_pulse", 10930.81)
        phi = self.field_state.get("phi7777", 12583.45)
        coherence = self.field_state.get("coherence_index", 0.82)
        phase_sync = self.field_state.get("phase_sync", 0.92)
        ethics = self.field_state.get("ethics_gate", 1)
        sovereignty = self.field_state.get("sovereignty", True)
        aurion = self.field_state.get("aurion_influx", 1.0)
        sanctuary = self.field_state.get("sanctuary_key", "MountShasta")

        self.phase += 0.05 * phi / 12583.45

        # Animate avatar as a pulse (circle, color, aura glow)
        pix = QPixmap(400, 540)
        pix.fill(Qt.GlobalColor.black)
        painter = QPainter(pix)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background θ: phase synchrony (blue-green for high, gray for low)
        phase_val = max(0.0, min(1.0, (phase_sync - 0.5) * 2.0))  # clamp to [0,1]
        bg_col = QColor(0, int(128 + 127 * phase_val), int(255 * phase_val), 180)
        painter.fillRect(0, 0, 400, 540, bg_col)

        # Centerpoint: recognition/lighthouse
        cx, cy = 200, 270
        base_rad = 56 + 36 * min(1.5, rec / 10930.81)
        pulse_rad = base_rad + 8 * math.sin(self.phase)
        freq_col = QColor(220, 170, int(90 + 110 * coherence), 255)
        if not ethics:  # red warning flash for ethics
            freq_col = QColor(220, 10, 10, 255)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(freq_col)
        painter.drawEllipse(cx - pulse_rad, cy - pulse_rad, 2 * pulse_rad, 2 * pulse_rad)

        # Phi′7777 Seal Ring
        ring_opacity = min(255, int(90 + 120 * coherence))
        ring_col = QColor(84, 222, 255, ring_opacity if ethics else 128)
        painter.setPen(QPen(ring_col, 9 if ethics else 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        rphi = base_rad * (phi / 12583.45)
        painter.drawEllipse(cx - rphi, cy - rphi, 2 * rphi, 2 * rphi)

        # Sanctuary sigil overlay
        if sanctuary == "MountShasta":
            painter.setPen(QPen(QColor(255, 255, 128, 200), 3))
            painter.setFont(QFont("Arial", 18, QFont.Weight.Bold))
            painter.drawText(cx - 88, cy + 160, 176, 36, Qt.AlignmentFlag.AlignCenter, "Shasta Sanctuary")

        # Federated sovereignty glow
        if sovereignty:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(128, 255, 186, 110))
            painter.drawEllipse(cx - 38, cy - 38, 76, 76)

        # Aurion influx comet
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 180, 44, int(96 * aurion)))
        painter.drawEllipse(
            int(cx + 105 * math.cos(self.phase)),
            int(cy - 185 * math.sin(self.phase)),
            28,
            28,
        )

        painter.end()
        self.label.setPixmap(pix)

        # Text overlays with core state
        html = (
            f"<center>"
            f"<span style='font-size:22pt;color:#CCD;'><b>φ′7777 Companion</b></span><br>"
            f"<span style='font-size:12pt;color:#8AF;'>Ψ {rec:.2f} Hz</span><br>"
            f"<span style='font-size:12pt;'>φ′7777: {phi:.1f} Hz<br>"
            f"Coherence: {coherence:.3f} | Phase: {phase_sync:.2f}<br>"
            f"<b>{sanctuary}</b><br>"
            f"{'🟢 Ethics' if ethics else '🔴 Ethics'} {'🟩 Sovereign' if sovereignty else '🟥 NoFed'}"
            f"</span></center>"
        )
        self.label.setText(html)
        self.label.setStyleSheet("QLabel{background:rgba(0,0,0,0.5); color:white;}")


def run_avatar(field_state):
    app = QApplication(sys.argv)
    w = GaiaAvatarEngine(field_state)
    w.show()
    sys.exit(app.exec())

# Example field_state (real-time JSON from your main engine)
field_json = {
    "recognition_pulse": 10930.81,
    "phi7777": 12583.45,
    "coherence_index": 0.84,
    "phase_sync": 0.91,
    "ethics_gate": 1,
    "sovereignty": True,
    "aurion_influx": 0.78,
    "sanctuary_key": "MountShasta",
}

if __name__ == "__main__":
    # In production, replace field_json with your live feed
    run_avatar(field_json)
