# llm-to-logic

Tried using deepseek to generate pddl from flow and pddl from flow and jsons. The outputs are have some differences 

Without json context:
```pddl
(:action add_payee
    :parameters (?u - user ?p - payee ?an - account_number ?pt - payee_type ?r - reference)
    :precondition (and
        (has_payee_name ?u ?p)
        (has_account_number ?u ?an)
        (has_payee_type ?u ?pt)
        (has_reference ?u ?r)
        (confirmed_details ?u)
    )
    :effect (and
        (payee_added ?u ?p)
    )
)

(:action utter_payee_added_success
    :parameters (?u - user ?p - payee)
    :precondition (and
        (payee_added ?u ?p)
    )
    :effect (and
        (notified_success ?u)
    )
)

(:action utter_payee_added_failure
    :parameters (?u - user)
    :precondition (and
        (not (payee_added ?u ?p))
    )
    :effect (and
        (notified_failure ?u)
    )
)
```
With json contexts

```pddl
(define (domain banking)
  (:types
    user
    account_number
    payeetype
    reference
  )

  (:predicates
    (user_exists ?u - user)
    (account_exists ?a - account_number)
    (payee_type_valid ?pt - payeetype)
    (confirmed_details ?u - user)
    (payee_added ?u - user ?pn - account_number ?pt - payeetype ?ref - reference)
  )

  (:action action_add_payee
    :parameters (?u - user ?pn - account_number ?pt - payeetype ?ref - reference)
    :precondition (and
        (user_exists ?u)
        (account_exists ?pn)
        (payee_type_valid ?pt)
        (confirmed_details ?u)
    )
    :effect (and
        (payee_added ?u ?pn ?pt ?ref)
    )
  )
)
```
