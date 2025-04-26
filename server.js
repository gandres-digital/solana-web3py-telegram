const express = require('express');
const { Connection, PublicKey, Keypair, Transaction, SystemProgram } = require('@solana/web3.js');
const bodyParser = require('body-parser');

const app = express();
const connection = new Connection("https://api.mainnet-beta.solana.com");

// Middleware para parsear JSON
app.use(bodyParser.json());

// Ruta para enviar tokens
app.post('/send', async (req, res) => {
    const { fromSecret, toAddress, amount } = req.body;

    try {
        // Crear la billetera de origen a partir de la clave secreta (debería ser un array)
        const fromWallet = Keypair.fromSecretKey(Uint8Array.from(fromSecret));
        const toWallet = new PublicKey(toAddress);

        // Crear la transacción
        const transaction = new Transaction().add(
            SystemProgram.transfer({
                fromPubkey: fromWallet.publicKey,
                toPubkey: toWallet,
                lamports: amount * 10 ** 9,  // Convertir el monto a lamports (1 SOL = 10^9 lamports)
            })
        );

        // Enviar la transacción
        const signature = await connection.sendTransaction(transaction, [fromWallet]);
        await connection.confirmTransaction(signature);

        res.send({ success: true, signature });
    } catch (error) {
        res.status(500).send({ success: false, error: error.message });
    }
});

// Iniciar el servidor en el puerto 3000
app.listen(3000, () => {
    console.log("Servidor de Solana corriendo en el puerto 3000");
});
