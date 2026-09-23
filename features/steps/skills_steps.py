"""Technical skills and skill-level steps."""

from behave import then


@then("the technical skill groups should be:")
def step_groups(context):
    actual = [g["title"] for g in context.site.technical_skill_groups()]
    assert actual == [row["group"] for row in context.table], f"groups were {actual}"


@then('the "{group}" group should mention "{tool}"')
def step_group_mentions(context, group, tool):
    groups = {g["title"]: g["description"] for g in context.site.technical_skill_groups()}
    assert group in groups, f"no such group {group!r}; got {sorted(groups)}"
    assert tool in groups[group], f"{group!r} does not mention {tool!r}"


@then("every technical skill group should have a description")
def step_groups_described(context):
    empty = [
        g["title"] for g in context.site.technical_skill_groups() if not g["description"]
    ]
    assert not empty, f"groups with no description: {empty}"


@then("the skill levels should be:")
def step_skill_levels(context):
    skills = {s["name"]: s for s in context.site.skills()}
    for row in context.table:
        name, expected = row["skill"], int(row["percentage"])
        assert name in skills, f"no such skill {name!r}; got {sorted(skills)}"
        assert skills[name]["value"] == expected, (
            f"{name}: expected {expected}, got {skills[name]['value']}"
        )
        assert skills[name]["label"] == f"{expected}%"


@then("every skill label should match its aria-valuenow")
def step_labels_match_aria(context):
    mismatched = [
        s["name"] for s in context.site.skills() if s["label"] != f"{s['value']}%"
    ]
    assert not mismatched, f"aria-valuenow disagrees with the label for: {mismatched}"
