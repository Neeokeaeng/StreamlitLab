mkdir -p ~/.streamlit/

echo "[theme]
primaryColor = ‘#E73030’
backgroundColor = ‘#F8F9E0’ 
secondaryBackgroundColor = ‘#E4E4E7’
textColor= ‘#3C3C3C’
font = ‘sans serif’
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
