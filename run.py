from app import create_app

app = create_app()

if __name__ == '__main__':
    # Em desenvolvimento, usamos debug=True
    # Host 0.0.0.0 permite acesso externo se necessário
    app.run(debug=True, host='0.0.0.0', port=5000)
