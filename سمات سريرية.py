import numpy as np
# !pip install scikit-fuzzy
import skfuzzy as fuzz  # المكتبة الصحيحة
from skfuzzy import control as ctrl
import sys
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')


# Inputs
hmb = ctrl.Antecedent(np.array([0, 1]), 'hmb')  # 0 = No, 1 = Yes
fibroid_size = ctrl.Antecedent(np.arange(0, 16, 0.1), 'fibroid_size')
uf_location = ctrl.Antecedent(np.arange(0, 3, 1), 'uf_location')  # 0 = submucosal, 1 = intramural, 2 = subserosal
md = ctrl.Antecedent(np.arange(2, 16, 0.1), 'md')  # 2–7 = normal, 8–15 = prolonged

# Outputs
anemia_risk = ctrl.Consequent(np.arange(0, 101, 1), 'anemia_risk')

# Fuzzy membership functions
hmb['no'] = fuzz.trimf(hmb.universe, [0, 0, 0.5])
hmb['yes'] = fuzz.trimf(hmb.universe, [0.5, 1, 1])

fibroid_size['small'] = fuzz.trapmf(fibroid_size.universe, [0, 0, 4, 6])
fibroid_size['medium'] = fuzz.trimf(fibroid_size.universe, [5, 8, 11])
fibroid_size['large'] = fuzz.trapmf(fibroid_size.universe, [10, 12, 15, 15])

uf_location['subserosal'] = fuzz.trimf(uf_location.universe, [0, 0, 0])
uf_location['intramural'] = fuzz.trimf(uf_location.universe, [1, 1, 1])
uf_location['submucosal'] = fuzz.trimf(uf_location.universe, [2, 2, 2])

uf_location['subserosal'] = fuzz.trimf(uf_location.universe, [2, 2, 2])

md['normal'] = fuzz.trapmf(md.universe, [2, 2, 6, 8])
md['prolonged'] = fuzz.trapmf(md.universe, [7, 9, 15, 15])

anemia_risk['very_low'] = fuzz.trimf(anemia_risk.universe, [0, 0, 20])
anemia_risk['low'] = fuzz.trimf(anemia_risk.universe, [10, 30, 50])
anemia_risk['moderate'] = fuzz.trimf(anemia_risk.universe, [40, 60, 80])
anemia_risk['high'] = fuzz.trapmf(anemia_risk.universe, [70, 90, 100, 100])

# Define fuzzy rules
rules1 = [
    ctrl.Rule(hmb['no'] & fibroid_size['small'] & uf_location['intramural'], anemia_risk['very_low']),
    ctrl.Rule(hmb['yes'] & fibroid_size['large'] & uf_location['submucosal'], anemia_risk['high']),
    ctrl.Rule(hmb['yes'] & fibroid_size['large'] & uf_location['intramural'], anemia_risk['moderate']),
    ctrl.Rule(hmb['no'] & fibroid_size['small'] & uf_location['submucosal'], anemia_risk['very_low']),
    ctrl.Rule(hmb['no'] & fibroid_size['medium'] & uf_location['subserosal'], anemia_risk['low']),
    ctrl.Rule(hmb['yes'] & fibroid_size['medium'], anemia_risk['moderate']),
    ctrl.Rule(md['prolonged'] & hmb['yes'], anemia_risk['high']),
    ctrl.Rule(md['prolonged'] & hmb['no'] & fibroid_size['small'], anemia_risk['moderate']),
    ctrl.Rule(hmb['no'] & fibroid_size['large'] & md['normal'], anemia_risk['low']),
    ctrl.Rule(fibroid_size['medium'] & uf_location['submucosal'] & md['prolonged'], anemia_risk['high']),
    ctrl.Rule(hmb['yes'] & fibroid_size['small'] & uf_location['submucosal'], anemia_risk['moderate'])
]


# Control System
anemia_ctrl = ctrl.ControlSystem(rules1)
anemia_sim = ctrl.ControlSystemSimulation(anemia_ctrl)


# Validation function
def validate_input(hmb, fibroid_size, uf_location, md):
    """
    Validate inputs based on predefined rules.
    Reject specific cases explicitly.
    """
    # رفض الحالات التي تلبي الشروط
    if uf_location == 2:  # تحت المخاطية
        if fibroid_size > 6 and hmb == 0:
            return False  # حجم الورم كبير ولا يوجد نزيف
        if fibroid_size < 1 and hmb == 1:
            return False  # حجم الورم صغير ويوجد نزيف
    if uf_location == 0 :
        if fibroid_size < 10 and (hmb == 1 or md > 7):
            return False


    # الحالات التي تمر الفحص
    return True

# Generate data
data = []
for i in range(1, 5000):
    try:
        hmb_value = np.random.choice([0, 1])  # نزيف
        fibroid_size_value = np.random.uniform(0, 16)  # حجم الورم
        uf_location_value = np.random.choice([0, 1, 2])  # موقع الورم
        md_value = np.random.uniform(2, 15)  # مدة الدورة

        if not validate_input(hmb_value, fibroid_size_value, uf_location_value, md_value):
            print(f"تم رفض الحالة {i}: القيم غير صالحة.")
            continue
        anemia_sim.input['hmb'] = hmb_value
        anemia_sim.input['fibroid_size'] = fibroid_size_value
        anemia_sim.input['uf_location'] = uf_location_value
        anemia_sim.input['md'] = md_value

        anemia_sim.compute()

        data.append([hmb_value, fibroid_size_value, uf_location_value, md_value, anemia_sim.output['anemia_risk']])

        print(f"الحالة {i}: hmb={hmb_value}, size={fibroid_size_value:.2f}, location={uf_location_value}, md={md_value:.2f}")
        print(f"خطر فقر الدم: {anemia_sim.output['anemia_risk']:.2f}")
        print("-" * 50)

    except Exception as e:
        print(f"خطأ في الحالة {i}: {str(e)}")
        print("-" * 50)

# Save to CSV
df = pd.DataFrame(data, columns=['HMB', 'fibroid_size', 'uf_location', 'MD', 'anemia_risk'])
df.to_csv('anemia_data_set.csv', index=False)