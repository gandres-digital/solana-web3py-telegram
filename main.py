from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import os


# Token del bot de Telegram (el que te dio BotFather)
TOKEN = "7949576925:AAGIixBC1FYGcRTOm4UD98oNTZXUGbgrAFg"

# Crear la aplicación con el token
application = Application.builder().token(TOKEN).build()

# Función para manejar el comando /send
async def send_tokens(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /send <dirección_destino> <monto>")
        return

    # Aquí no necesitamos la clave privada, solo la pública para la transacción
    to_address = context.args[0]  # Dirección de destino
    amount = float(context.args[1])  # Monto a enviar

    try:
        # Realizar la solicitud POST al servidor Node.js (que manejará la clave privada)
        response = requests.post("http://localhost:3000/send", json={
            "toAddress": to_address,
            "amount": amount
        })

        if response.status_code == 200:
            # Si la respuesta es exitosa, devolver la transacción
            tx_signature = response.json().get("signature")
            await update.message.reply_text(f"Tokens enviados exitosamente. Transacción: {tx_signature}")
        else:
            # En caso de error, responder con el mensaje de error
            error_message = response.json().get("error", "Error desconocido")
            await update.message.reply_text(f"Error al enviar tokens: {error_message}")
    except Exception as e:
        await update.message.reply_text(f"Error al conectar con el servidor: {e}")

# Registrar el comando /send
application.add_handler(CommandHandler("send", send_tokens))

# Iniciar el bot
application.run_polling()
