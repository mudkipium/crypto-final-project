package main

import (
    "crypto/aes"
    "crypto/rand"
    "crypto/sha256"
    "encoding/hex"
    "flag"
    "fmt"
    "io/ioutil"
    "os"
    "strings"
)

func main() {
    // Retrieves command line arguments
    var key, input, output string
    flags := flag.NewFlagSet("", flag.ExitOnError)
    flags.StringVar(&key, "k", "no key", "the key")
    flags.StringVar(&input, "i", "no input file", "the input file path")
    flags.StringVar(&output, "o", "no output file", "the output file path")
    flags.Parse(os.Args[2:])
    mode := os.Args[1]

    bytekey, err := hex.DecodeString(key)
    if err != nil {
        fmt.Println("Error decoding key.")
        os.Exit(1)
    }
    if len(bytekey) != 32 {
        fmt.Println("Key is not 32 bytes.")
        os.Exit(1)
    }

    fileContents, err := ioutil.ReadFile(input)
    if err != nil {
        fmt.Println("Error reading file:", err)
        os.Exit(1)
    }
    fileString := string(fileContents)

    if strings.Compare("encrypt", mode) == 0 {
        cipheredBytes := runEncrypt(bytekey, fileString)
        err := ioutil.WriteFile(output, cipheredBytes, 0644)
        if err != nil {
            fmt.Println("Error writing file:", err)
            os.Exit(1)
        }
    } else if strings.Compare("decrypt", mode) == 0 {
        plainText := runDecrypt(bytekey, fileString)
        out, err := os.Create(output)
        if err != nil {
            fmt.Println("Error creating file:", err)
            os.Exit(1)
        }
        _, err = out.WriteString(plainText)
        if err != nil {
            fmt.Println("Error writing file:", err)
            os.Exit(1)
        }
    } else {
        fmt.Println("Invalid mode. Should be encrypt or decrypt.")
        os.Exit(1)
    }
}

func runEncrypt(key []byte, message string) ([]byte) {
    kEnc := key[0:aes.BlockSize]
    kMac := key[aes.BlockSize:]
    messageBytes := []byte(message)
    messageBytes = append(messageBytes, HMAC_SHA256(kMac, messageBytes)...)
    n := len(messageBytes) % aes.BlockSize
    for i := 0; i < aes.BlockSize - n; i++ {
            messageBytes = append(messageBytes, byte(aes.BlockSize - n))
    }
    return CBC_Encrypt(kEnc, messageBytes)
}

func CBC_Encrypt(kEnc []byte, messageBytes []byte) ([]byte) {
    // Declaring variables
    offset := 0
    IV := make([]byte, aes.BlockSize)
    cipheredBytes := make([]byte, aes.BlockSize + len(messageBytes))
    block, err := aes.NewCipher(kEnc)
    if (err != nil) {
        fmt.Println(err)
        os.Exit(1)
    }
    // CBC encryption
    for offset < len(messageBytes) {
        // If this is the first block, use randomly generated IV
        if offset == 0 {
            rand.Read(IV)
            for i := 0; i < aes.BlockSize; i++ {
                cipheredBytes[i] = IV[i]
            }
        } else {
            // Otherwise, the IV is the previous block (maps to current indices bc IV in front)
            IV = cipheredBytes[offset:offset + aes.BlockSize]
        }
        // XOR current message block with IV
        for i := 0; i < aes.BlockSize; i++ {
            messageBytes[offset + i] = messageBytes[offset + i] ^ IV[i]
        }
        // Encrypt current block
        block.Encrypt(cipheredBytes[offset + aes.BlockSize:offset + (2 * aes.BlockSize)],
            messageBytes[offset:offset + aes.BlockSize])
        offset += 16
    }
    return cipheredBytes
}

func HMAC_SHA256(kMac []byte, messageBytes []byte) ([]byte) {
    // Declaring variables
    BLOCKSIZE := 64
    ipad := byte(0x36)
    opad := byte(0x5c)
    var kMacIpad, kMacOpad []byte
    // Padding MAC key up to 32 bytes
    for len(kMac) < BLOCKSIZE {
        kMac = append(kMac, byte(0))
    }
    // H((kMAC ^ ipad) || message)
    for i := range kMac {
        kMacIpad = append(kMacIpad, kMac[i] ^ ipad)
        kMacOpad = append(kMacOpad, kMac[i] ^ opad)
    }
    h1 := sha256.New()
    h1.Write(append(kMacIpad, messageBytes...))
    shaMacAndText := h1.Sum(nil)
    // H((kMac ^ opad) || H((kMAC ^ iPad) || message))
    h2 := sha256.New()
    h2.Write(append(kMacOpad, shaMacAndText...))
    return h2.Sum(nil)
}

func runDecrypt(key []byte, ciphertext string) (string) {
    kEnc := key[:aes.BlockSize]
    kMac := key[aes.BlockSize:]
    decryptedBytes := CBC_Decrypt(kEnc, []byte(ciphertext))
    decryptedBytes, pad_err := checkPadding(decryptedBytes)
    mac_err := checkMAC(kMac, decryptedBytes)
    if ((pad_err + mac_err) != "") {
        print("DECRYPTION ERROR")
        os.Exit(1)
    }
    return string(decryptedBytes[:len(decryptedBytes) - 32])
}

func CBC_Decrypt(kEnc []byte, cipheredBytes []byte) ([]byte) {
    offset := 0
    IV := cipheredBytes[:aes.BlockSize]
    messageBytes := cipheredBytes[aes.BlockSize:]
    decryptedBytes := make([]byte, len(messageBytes))
    block, err := aes.NewCipher(kEnc)
    if (err != nil) {
        fmt.Println(err)
        os.Exit(1)
    }

    for offset < len(messageBytes) {
        block.Decrypt(decryptedBytes[offset:offset + aes.BlockSize],
            messageBytes[offset:offset + aes.BlockSize])
        if offset > 0 {
            IV = messageBytes[offset - aes.BlockSize:offset]
        }
        for i := 0; i < aes.BlockSize; i++ {
            decryptedBytes[offset + i] = decryptedBytes[offset + i] ^ IV[i]
        }
        offset += 16
    }
    return decryptedBytes
}

func checkPadding(decryptedBytes []byte) ([]byte, string) {
    err := ""
    n := int(decryptedBytes[len(decryptedBytes) - 1])
    if n > aes.BlockSize {
        err = "INVALID PADDING"
    }
    for i := len(decryptedBytes) - n; i < len(decryptedBytes); i++ {
        if int(decryptedBytes[i]) != n {
            err = "INVALID PADDING"
        }
    }
    return decryptedBytes[:len(decryptedBytes) - n], err
}

func checkMAC(kMac []byte, decryptedBytes []byte) (string) {
    err := ""
    MAC := decryptedBytes[len(decryptedBytes) - 32:]
    message := decryptedBytes[:len(decryptedBytes) - 32]
    actualMAC := HMAC_SHA256(kMac, message)
    for i := 0; i < 32; i++ {
        if MAC[i] != actualMAC[i] {
            err = "INVALID MAC"
        }
    }
    return err
}
