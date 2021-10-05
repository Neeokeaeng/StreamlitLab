mkdir -p ~/.streamlit/

echo "[theme]
primaryColor = ‘#E73030’
backgroundColor = ‘#F8F9E0’ 
secondaryBackgroundColor = ‘#fafafa’
textColor= ‘#424242’
font = ‘sans serif’
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
