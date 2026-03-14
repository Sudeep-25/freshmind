import streamlit as st
import re
from datetime import date
from mock_data import get_all_items, get_expiring_items

st.set_page_config(page_title="FreshMind", layout="wide")

st.sidebar.title("FreshMind - Smart Pantry")
st.sidebar.markdown("*Your Smart Pantry Assistant*")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", ["Pantry", "Add Item", "AI Recipes", "Dashboard"])
st.sidebar.markdown("---")
st.sidebar.caption("FreshMind v1.0 | Person B Frontend")

def parse_quantity(qty_str):
    numbers = re.findall(r'\d+\.?\d*', str(qty_str))
    units = re.findall(r'[a-zA-Z]+', str(qty_str))
    number = float(numbers[0]) if numbers else 0
    unit = units[0] if units else "pcs"
    return number, unit

def show_pantry():
    st.title("My Pantry")
    items = get_all_items()
    if not items:
        st.warning("Your pantry is empty!")
        return
    today = date.today()
    total = len(items)
    expiring_soon = len([i for i in items if (i["expiry_date"] - today).days <= 7])
    critical = len([i for i in items if (i["expiry_date"] - today).days <= 3])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Items", total)
    with col2:
        st.metric("Expiring This Week", expiring_soon)
    with col3:
        st.metric("Critical (< 3 days)", critical)

    st.markdown("---")
    st.markdown("**Color Guide:** 🔴 Less than 3 days   🟠 Less than 7 days   🟢 Safe")
    st.markdown("---")

    for item in items:
        days_left = (item["expiry_date"] - today).days
        if days_left <= 3:
            color = "#ffcccc"
            badge = "URGENT"
        elif days_left <= 7:
            color = "#ffe5cc"
            badge = "SOON"
        else:
            color = "#ccffcc"
            badge = "SAFE"

        st.markdown(
            f"""<div style="background-color: {color}; padding: 12px 20px;
            border-radius: 8px; margin-bottom: 8px;">
            <b>{item['name']}</b> | {item['category']} |
            Qty: {item['quantity']} | Expires: {item['expiry_date']} |
            Days left: <b>{days_left}</b> | {badge}
            </div>""",
            unsafe_allow_html=True
        )

        current_num, current_unit = parse_quantity(item["quantity"])
        col_qty, col_used, col_btn, col_del = st.columns([2, 2, 1, 1])

        with col_qty:
            st.markdown(f"**Current:** {item['quantity']}")

        with col_used:
            used = st.number_input(
                f"Amount used ({current_unit})",
                min_value=0.0,
                max_value=float(current_num),
                value=0.0,
                step=1.0,
                key=f"used_{item['id']}"
            )

        with col_btn:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Update", key=f"upd_{item['id']}"):
                remaining = current_num - used
                if remaining <= 0:
                    st.error(f"{item['name']} is finished! Please delete it.")
                else:
                    st.success(f"Updated! {item['name']} remaining: {remaining}{current_unit}")

        with col_del:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Delete", key=f"del_{item['id']}"):
                st.warning(f"{item['name']} deleted! (backend needed)")

    st.markdown("---")
    expiring = get_expiring_items(days=7)
    if expiring:
        st.error(f"Warning: {len(expiring)} item(s) expiring within 7 days!")

if page == "Pantry":
    show_pantry()
elif page == "Add Item":
    st.title("Add New Item")
    st.info("Coming Day 3")
elif page == "AI Recipes":
    st.title("AI Recipe Suggestions")
    st.info("Coming Day 4")
elif page == "Dashboard":
    st.title("Dashboard")
    st.info("Coming Day 5")
