### Utility functions
def eq(x, y):
    return x == y

def gt(x, y):
    return x > y

def lt(x, y):
    return x < y

def boolean(string):
    if string == 'True':
        return True
    if string == 'False':
        return False
    raise ValueError('bool must be True or False')


### Setting up initial data

def define_contexts(sh):
    sh.define_context(Context('patient', ['name', 'sex', 'age']))
    sh.define_context(Context('symptom', ['temp', 'breath-condition', 'cough-condition', 'days-old']))
    
    #Goal:
    sh.define_context(Context('virus', goals=['identity']))

def define_params(sh):
    # Patient params
    sh.define_param(Parameter('name', 'patient', cls=str, ask_first=True))
    sh.define_param(Parameter('sex', 'patient', enum=['female', 'male'], ask_first=True))
    sh.define_param(Parameter('age', 'patient', cls=int, ask_first=True))
        ## Advanced params
    sh.define_param(Parameter('outside-activity', 'patient', cls=boolean))
    sh.define_param(Parameter('contact-condition', 'patient', cls=boolean))
    sh.define_param(Parameter('travel-activity', 'patient', cls=boolean))
    sh.define_param(Parameter('animal-bite-activity', 'patient', cls=boolean))
    
    # Symptom params
    sh.define_param(Parameter('temp', 'symptom', cls=int, ask_first=True))
    sh.define_param(Parameter('breath-condition', 'symptom', cls=boolean, ask_first=True))
    sh.define_param(Parameter('cough-condition', 'symptom', cls=boolean, ask_first=True))
    sh.define_param(Parameter('days-old', 'symptom', cls=int, ask_first=True))
        ## Advanced params
    sh.define_param(Parameter('vomit-condition', 'symptom', cls=boolean))   
    sh.define_param(Parameter('diarrhea-condition', 'symptom', cls=boolean))
    sh.define_param(Parameter('community-condition', 'symptom', cls=boolean))
    sh.define_param(Parameter('headache-condition', 'symptom', cls=boolean))
    sh.define_param(Parameter('muscle-condition', 'symptom', cls=boolean))
    sh.define_param(Parameter('throat-condition', 'symptom', cls=boolean))
    sh.define_param(Parameter('mental-condition', 'symptom', enum=['confusion','tired','anxious']))
    sh.define_param(Parameter('oral-ulcers-condition', 'symptom', cls=boolean))
    

    # Virus params
    Virus = ['COVID-19', 'Ebola', 'Flu', 'Cold', 'H1N1','Rabies','HIV','SARS']
    sh.define_param(Parameter('identity', 'virus', enum=Virus, ask_first=True))
        ## Professional test params
    sh.define_param(Parameter('antibody test result', 'virus', enum=['positive', 'negative']))
    
    #sh.define_param(Parameter('aerobicity', 'virus', enum=['aerobic', 'anaerobic']))
    #sh.define_param(Parameter('growth-conformation', 'virus',
    #                          enum=['chains', 'pairs', 'clumps']))

def define_rules(sh):
    sh.define_rule(Rule(1,
                        [
                            ('temp', 'symptom', gt, 37),
                            ('breath-condition','symptom', eq, True),
                            ('cough-condition','symptom', eq, True),
                            ('days-old', 'symptom', gt, 7),

                            ('vomit-condition', 'symptom', eq, True),
                            ('diarrhea-condition','symptom', eq, True),
                            ('outside-activity', 'patient', eq, True),
                            ('travel-activity','patient', eq, True),
                            
                         ],
                        [
                            ('identity', 'virus', eq, 'COVID-19')
                        ],
                        0.7))
    sh.define_rule(Rule(2,
                        [
                            ('temp', 'symptom', gt, 37),
                            ('headache-condition','symptom', eq, True),
                            ('muscle-condition','symptom', eq, True),
                            ('throat-condition','symptom', eq, True),
                            ('days-old', 'symptom', gt, 7),

                            ('vomit-condition', 'symptom', eq, True),
                            ('diarrhea-condition','symptom', eq, True),
                            ('outside-activity', 'patient', eq, True),
                            ('travel-activity','patient', eq, True),
                            
                         ],
                        [
                            ('identity', 'virus', eq, 'Ebola')
                        ],
                        0.7))        
    sh.define_rule(Rule(3,
                        [
                            ('temp', 'symptom', gt, 37),
                            ('headache-condition','symptom', eq, True),
                            ('muscle-condition','symptom', eq, True),
                            ('throat-condition','symptom', eq, True),
                            ('days-old', 'symptom', lt, 5)    
                         ],
                        [('identity', 'virus', eq, 'Flu')],
                        0.5))
    sh.define_rule(Rule(4,
                        [
                            ('headache-condition','symptom', eq, False),
                            ('muscle-condition','symptom', eq, False),
                            ('throat-condition','symptom', eq, True),
                            ('days-old', 'symptom', gt, 3)    
                         ],
                        [('identity', 'virus', eq, 'Cold')],
                        0.7))
    sh.define_rule(Rule(5,
                        [
                            ('temp', 'symptom', gt, 37),
                            ('cough-condition','symptom', eq, True),
                            ('headache-condition','symptom', eq, True),
                            ('muscle-condition','symptom', eq, False),
                            ('throat-condition','symptom', eq, True),
                            ('days-old', 'symptom', gt, 7),

                            ('vomit-condition', 'symptom', eq, True),
                            ('diarrhea-condition','symptom', eq, True),
                            
                         ],
                        [('identity', 'virus', eq, 'H1N1')],
                        0.7))
    sh.define_rule(Rule(6,
                        [
                            ('temp', 'symptom', gt, 37),
                            ('headache-condition','symptom', eq, True),
                            ('muscle-condition','symptom', eq, False),
                            ('mental-condition','symptom',eq, 'confusion'),
                            ('days-old', 'symptom', gt, 3),
                            ('vomit-condition', 'symptom', eq, True),
                            ('animal-bite-activity', 'patient', eq, True),
                            
                         ],
                        [('identity', 'virus', eq, 'Rabies')],
                        0.7))
    sh.define_rule(Rule(7,
                        [
                            ('temp', 'symptom', gt, 37),
                            ('throat-condition','symptom', eq, True),
                            ('muscle-condition','symptom', eq, True),
                            ('days-old', 'symptom', gt, 7),

                            ('vomit-condition', 'symptom', eq, True),
                            ('diarrhea-condition','symptom', eq, True),
                            ('mental-condition','symptom',eq, 'tired'),
                            ('oral-ulcers-condition','symptom',eq, True),
                            
                         ],
                        [('identity', 'virus', eq, 'HIV')],
                        0.7))
    sh.define_rule(Rule(8,
                        [
                            ('temp', 'symptom', gt, 37),
                            ('breath-condition','symptom', eq, True),
                            ('cough-condition','symptom', eq, True),
                            ('muscle-condition','symptom', eq, True),
                            ('headache-condition','symptom', eq, True),
                            ('days-old', 'symptom', gt, 7),
                            
                         ],
                        [('identity', 'virus', eq, 'SARS')],
                        0.7))
### Running the system

import logging
from emycin import Parameter, Context, Rule, Shell

def report_findings(findings):
    for inst, result in findings.items():
        print('Findings for %s-%d:' % (inst[0], inst[1]))
        for param, vals in result.items():
            possibilities = ['%s: %f' % (val[0], val[1]) for val in vals.items()]
            print('%s: %s' % (param, ', '.join(possibilities)))
        
def main():
    sh = Shell()
    define_contexts(sh)
    define_params(sh)
    define_rules(sh)
    report_findings(sh.execute(['patient', 'symptom', 'virus']))
    
main()