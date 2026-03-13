import streamlit as st
import pandas as pd
from datetime import date
from mock_data import get_all_items, get_expiring_items

st.set_page_config(page_title="FreshMind", page_icon="", layout="wide")

st.sidebar.title("FreshMind - Smart Pantry")
st.sidebar.markdown("*Your Smart Pantry Assistant*")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["Pantry", "Add Item", "AI Recipes", "Dashboard"]
)

st.sidebar.markdown("---")
st.sidebar.caption("FreshMind v1.0 | Person B Frontend")


# ─────────────────────────────────────────
# PAGE 1 — PANTRY VIEW
# ─────────────────────────────────────────
def show_pantry():
    st.title("My Pantry")

    # Get all items from mock data
    items = get_all_items()

    if not items:
        st.warning("Your pantry is empty! Add some items.")
        return

    # Show summary numbers at top
    today = date.today()
    total = len(items)
    expiring_soon = len([i for i in items if (i["expiry_date"] - today).days <= 7])
    critical = len([i for i in items if (i["expiry_date"] - today).days <= 3])

    # 3 metric boxes at top
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Items", total)
    with col2:
        st.metric("Expiring This Week", expiring_soon)
    with col3:
        st.metric("Critical (< 3 days)", critical)

    st.markdown("---")

    # Color legend
    st.markdown("""
    **Color Guide:**
    🔴 Expires in less than 3 days &nbsp;&nbsp;
    🟠 Expires in less than 7 days &nbsp;&nbsp;
    🟢 Safe
    """)

    st.markdown("---")

    # Show each item as a colored row
    for item in items:
        days_left = (item["expiry_date"] - today).days

        # Decide color based on days left
        if days_left <= 3:
            color = "#ffcccc"    # red background
            badge = "🔴 URGENT"
        elif days_left <= 7:
            color = "#ffe5cc"    # orange background
            badge = "🟠 SOON"
        else:
            color = "#ccffcc"    # green background
            badge = "🟢 SAFE"

        # Display item card
        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color: {color};
                    padding: 12px 20px;
                    border-radius: 8px;
                    margin-bottom: 8px;
                ">
                    <b>{item['name']}</b> &nbsp;|&nbsp;
                    {item['category']} &nbsp;|&nbsp;
                    Qty: {item['quantity']} &nbsp;|&nbsp;
                    Expires: {item['expiry_date']} &nbsp;|&nbsp;
                    Days left: <b>{days_left}</b> &nbsp;|&nbsp;
                    {badge}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Delete button for each item
            if st.button(f"Delete {item['name']}", key=f"del_{item['id']}"):
                st.warning(f"{item['name']} would be deleted (backend needed!)")

    st.markdown("---")

    # Show expiring items alert box at bottom
    expiring = get_expiring_items(days=7)
    if expiring:
        st.error(f"⚠️ {len(expiring)} item(s) expiring within 7 days — consider using them soon!")


# ─────────────────────────────────────────
# PAGE ROUTER
# ─────────────────────────────────────────
if page == "Pantry":
    show_pantry()

elif page == "Add Item":
    st.title("Add New Item")
    st.info("Add Item Form - Coming Day 3")

elif page == "AI Recipes":
    st.title("AI Recipe Suggestions")
    st.info("AI Recipes - Coming Day 4")

elif page == "Dashboard":
    st.title("Dashboard")
    st.info("Charts - Coming Day 5")
