# Trello Updater

This runs a service that trello can access. Modules can be written for more functionality. Triggers match the REST response that comes in, while tasks are specific to each module. Templating is allowed and can either be based on the current trigger context, or additional context can be bound with the name option on a task, namespacing with the name. This follows basic Jinja so filters and tests are available as well. Keys can be rolled up so {"foo:bar:baz": true} will parse to {"foo": {"bar": {"baz": true}}}. Additional modules include timer (cron and sleep), github webhook, and shell command task. Modules can be easily made, see Timer for an example.

```
fill_in_groceries:
  triggers:
  - trello:
      type: createCard
      data:card:name: Groceries
  tasks:
  - trello:addLabel:
      card: "{{ data.card.id }}"
      label: Planning
  - name: create_card
    trello:createCard:
      name: Weekend Tidy
      list: Weekend
  - trello:createChecklist:
      card: "{{ create_card.id }}"
      name: General
```
