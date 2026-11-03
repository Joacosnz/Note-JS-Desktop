import os
import re
import sys

with open('frontend/styles.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Search for any rule matching toolbar buttons that sets amber color
toolbar_button_ids = ['btn-in-note-search', 'btn-pin-note', 'btn-page-appearance', 'btn-reopen-panels']

for b_id in toolbar_button_ids:
    # Check if ID appears in an amber rule
    for match in re.finditer(r'([^\{\}]+)\{([^\{\}]+)\}', css):
        selectors = match.group(1)
        body = match.group(2)
        if f'#{b_id}' in selectors:
            if 'var(--accent-amber' in body or '#f59e0b' in body:
                print(f"FAILED: #{b_id} found in amber rule: {selectors.strip()}")
                sys.exit(1)

print("PASS: None of the non-insert toolbar button IDs appear in any amber CSS rule.")

# 2. Check the global amber secondary button selector
global_amber_match = re.search(
    r'(\.btn-secondary:not\(\.btn-trash-action\):not\(\.btn-danger\):not\(\[class\*="trash"\]\):not\(\[class\*="delete"\]\)[^\{]*)\{([^\{\}]+)\}',
    css
)
if not global_amber_match:
    print("FAILED: Global amber rule not found in styles.css")
    sys.exit(1)

global_sel = global_amber_match.group(1)
print(f"Global amber selector: {global_sel.strip()}")

# Must exclude toolbar classes
for cls in [':not(.format-bar-action-icon-btn)', ':not(.in-note-find-trigger)', ':not(.page-dots-btn)']:
    if cls not in global_sel:
        print(f"FAILED: Global amber rule does not exclude {cls}")
        sys.exit(1)

print("PASS: Global amber rule explicitly excludes all format bar secondary button classes.")

# 3. Check Section 6 override position and specificity
sec6_match = re.search(
    r'(\.desktop-format-bar\s+button\.btn-secondary[^\}]+\.desktop-format-bar\s+\.btn-secondary:not\(\.btn-trash-action\))\s*\{([^\{\}]+)\}',
    css
)
if not sec6_match:
    print("FAILED: Section 6 format bar neutral override not found")
    sys.exit(1)

sec6_pos = sec6_match.start()
global_pos = global_amber_match.start()

if sec6_pos <= global_pos:
    print("FAILED: Section 6 appears before global amber rule, should be after!")
    sys.exit(1)

sec6_body = sec6_match.group(2)
if 'background: transparent !important' not in sec6_body:
    print("FAILED: Section 6 does not specify background: transparent !important")
    sys.exit(1)

if 'color: var(--text-secondary) !important' not in sec6_body:
    print("FAILED: Section 6 does not specify color: var(--text-secondary) !important")
    sys.exit(1)

print("PASS: Section 6 format bar neutral rule is positioned AFTER global amber rule with !important.")

# 4. Check hover and active rules in Section 6
sec6_hover = re.search(r'\.desktop-format-bar\s+\.btn-secondary:not\(\.btn-trash-action\):hover\s*\{([^\{\}]+)\}', css)
if not sec6_hover or 'background: var(--bg-elevated) !important' not in sec6_hover.group(1):
    print("FAILED: Section 6 hover rule missing or not neutral")
    sys.exit(1)

sec6_active = re.search(r'\.desktop-format-bar\s+\.btn-secondary:not\(\.btn-trash-action\)\.active\s*\{([^\{\}]+)\}', css)
if not sec6_active or 'background: var(--bg-elevated) !important' not in sec6_active.group(1):
    print("FAILED: Section 6 active rule missing or not neutral")
    sys.exit(1)

print("PASS: Section 6 hover and active rules correctly use var(--bg-elevated) !important.")

# 5. Check #btn-insert-dropdown amber rules
insert_dropdown_match = re.search(r'(?:#btn-insert-dropdown|\.insert-dropdown-btn)\s*\{([^\{\}]+)\}', css)
if not insert_dropdown_match or 'var(--accent-amber' not in insert_dropdown_match.group(1):
    print("FAILED: #btn-insert-dropdown amber styling missing in styles.css")
    sys.exit(1)

print("PASS: #btn-insert-dropdown has amber styling correctly defined.")
print("ALL FORMAT BAR CHECKS PASSED EMPIRICALLY.")
