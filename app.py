import streamlit as st
from graphviz import Digraph

# Initialize session state
if 'stats' not in st.session_state:
    st.session_state.stats = {'cash': 1000000, 'ownership': 1.0, 'debt': 0, 'risk': 0}
if 'step' not in st.session_state:
    st.session_state.step = 'start'

def restart_game():
    st.session_state.stats = {'cash': 1000000, 'ownership': 1.0, 'debt': 0, 'risk': 0}
    st.session_state.step = 'start'

st.title("Debt vs. Equity - Decision Tree Quiz Game (with Flowchart)")

# Structure the decision tree as a dictionary
decision_tree = {
    'start': {
        'question': "You need $1M for expansion. Choose your financing method:",
        'choices': {
            "Take $1M Debt at 6%": ({'debt': 1000000, 'risk': 0.2}, 'debt_scenario'),
            "Sell 20% Equity": ({'ownership': -0.2}, 'equity_scenario')
        }
    },
    'debt_scenario': {
        'question': "Debt financing chosen. A downturn hits and cash flow is tight. What do you do?",
        'choices': {
            "Take $500K Bridge Loan at 8%": ({'debt': 500000, 'risk': 0.3}, 'results'),
            "Sell 10% Equity": ({'ownership': -0.1, 'risk': -0.1}, 'results')
        }
    },
    'equity_scenario': {
        'question': "Equity financing chosen. Investors want dividends in a booming market. What do you do?",
        'choices': {
            "Pay Dividends (reduce cash flow)": ({'cash': -200000, 'risk': 0.1}, 'results'),
            "Reinvest profits for growth": ({'ownership': -0.05, 'risk': -0.1}, 'results')
        }
    }
}

def update_stats(changes):
    for key, value in changes.items():
        if key in st.session_state.stats:
            st.session_state.stats[key] += value
        else:
            st.session_state.stats[key] = value

def draw_tree(current_node):
    dot = Digraph(comment='Decision Tree')
    # Tree structure
    dot.node('start', 'Start: Choose Financing')
    dot.node('debt_scenario', 'Debt Scenario')
    dot.node('equity_scenario', 'Equity Scenario')
    dot.node('results', 'Results')
    dot.edge('start', 'debt_scenario', label='Take Debt')
    dot.edge('start', 'equity_scenario', label='Sell Equity')
    dot.edge('debt_scenario', 'results', label='Bridge Loan')
    dot.edge('debt_scenario', 'results', label='Sell Equity')
    dot.edge('equity_scenario', 'results', label='Pay Dividends')
    dot.edge('equity_scenario', 'results', label='Reinvest')
    # Highlight current node
    if current_node:
        dot.node(current_node, color='red', style='filled', fillcolor='lightpink')
    st.graphviz_chart(dot)

# Main logic
if st.session_state.step in decision_tree:
    node = decision_tree[st.session_state.step]
    st.write(node['question'])
    for choice_text, (stat_effects, next_node) in node['choices'].items():
        if st.button(choice_text):
            update_stats(stat_effects)
            st.session_state.step = next_node

elif st.session_state.step == 'results':
    st.write("### Results:")
    st.write(f"Ownership retained: {st.session_state.stats['ownership'] * 100:.1f}%")
    st.write(f"Total debt: ${st.session_state.stats['debt']:,}")
    st.write(f"Company cash: ${st.session_state.stats['cash']:,}")
    st.write(f"Risk level: {st.session_state.stats['risk']:.2f} (higher is riskier)")
    if st.button("Restart Game"):
        restart_game()

# Always show flowchart
st.write("### Current Decision Tree")
draw_tree(st.session_state.step)

# Live feedback sidebar
with st.sidebar:
    st.header("Current Stats")
    st.write(f"Cash: ${st.session_state.stats['cash']:,}")
    st.write(f"Ownership: {st.session_state.stats['ownership'] * 100:.1f}%")
    st.write(f"Debt: ${st.session_state.stats['debt']:,}")
    st.write(f"Risk: {st.session_state.stats['risk']:.2f}")

st.markdown("---")
st.markdown("Restart to explore different decision paths and their effects.")

