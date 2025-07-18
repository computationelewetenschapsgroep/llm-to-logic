from encoder.rasa_encoding import DomainEncoding
from encoder.rasa_encoding.variant import Variant

problem_variant = Variant()
domain_encoding =  DomainEncoding(variant = problem_variant)

for action in domain_encoding.domain.actions:
    print(action.to_pddl())