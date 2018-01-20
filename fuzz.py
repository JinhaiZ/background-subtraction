import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class Fuzzy():

    def __init__(self):
        # New Antecedent/Consequent objects hold universe variables and membership
        # functions
        f1 = ctrl.Antecedent(np.arange(0, 1.05, 0.05), 'Average of the generated background(F1)')
        f2 = ctrl.Antecedent(np.arange(0, 1.05, 0.05), 'Sum of difference values between backgroud and input image(F2)')
        p = ctrl.Consequent(np.arange(0, 1.05, 0.05), 'Output optimal threshold(p)')

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        f1['Low'] = fuzz.trimf(f1.universe, [0, 0, 0.4])
        f1['Medium'] = fuzz.trimf(f1.universe, [0.3, 0.5, 0.7])
        f1['High'] = fuzz.trimf(f1.universe, [0.6, 1, 1])

        #f1.view()

        f2['Low'] = fuzz.trimf(f2.universe, [0.0, 0.0, 0.65])
        f2['High'] = fuzz.trimf(f2.universe, [0.35, 1, 1])

        #f2.view()

        p['Very Low'] = fuzz.trapmf(p.universe, [0, 0, 0.1, 0.2])
        p['Low'] = fuzz.trimf(p.universe, [0.15, 0.25, 0.35])
        p['Medium'] = fuzz.trimf(p.universe, [0.3, 0.4, 0.5])
        p['High'] = fuzz.trimf(p.universe, [0.45, 0.55, 0.65])
        p['Very High'] = fuzz.trapmf(p.universe, [0.6, 0.7, 1, 1])

        #p.view()
        # You can see how these look with .view()
        rule1 = ctrl.Rule(f1['Low'] & f2['Low'], p['Low'])
        rule2 = ctrl.Rule(f1['Low'] & f2['High'], p['Very High'])
        rule3 = ctrl.Rule(f1['Medium'] & f2['Low'], p['Medium'])
        rule4 = ctrl.Rule(f1['Medium'] & f2['High'], p['Medium'])
        rule5 = ctrl.Rule(f1['High'] & f2['Low'], p['High'])
        rule6 = ctrl.Rule(f1['High'] & f2['High'], p['Very Low'])

        threshold_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
        self.threshold = ctrl.ControlSystemSimulation(threshold_ctrl)

    def get_threshold(self, f1, f2):
        # compute optimal threshold given f1 and f2 value
        #print "f1=", f1, ", f2=" ,f2
        
        self.threshold.input['Average of the generated background(F1)'] = f1
        self.threshold.input['Sum of difference values between backgroud and input image(F2)'] = f2

        # Crunch the numbers
        self.threshold.compute()
        #p.view(sim=threshold)
        return self.threshold.output['Output optimal threshold(p)']
        