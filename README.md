![Demo](loos.jpg)


# uterine-fibroid-anemia-detection
Deep learning model for anemia risk prediction in women with uterine fibroids


# 🧬 Uterine Fibroid Anemia Risk Prediction

## 📌 Overview
This project presents a **deep learning-based approach** for predicting **anemia risk** in women suffering from **uterine fibroids** using clinical features.

The model is designed to support **medical research and decision-making**, not as a diagnostic replacement.

---

## 🧠 Model Description
- Architecture: **1D Convolutional Neural Network (CNN)**
- Framework: **TensorFlow / Keras**
- Task: Regression (Anemia Risk Prediction)

---

## 📊 Dataset Features
| Feature | Description |
|------|-----------|
| HMB | Heavy Menstrual Bleeding |
| fibroid_size | Size of uterine fibroid |
| uf_location | Fibroid location |
| MD | Menstrual duration |
| anemia_risk | Target variable |

> ⚠ Dataset not included for privacy reasons.

---

## 🛠 Tech Stack
- Python
- TensorFlow / Keras
- Scikit-learn
- Pandas / NumPy
- Matplotlib

---

## 🚀 How to Run
```bash
pip install -r requirements.txt
python model.py
