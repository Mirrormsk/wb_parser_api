import qrcode


def generate_qr(data: str, filename: str) -> None:
    """
    Generates a qr code and saves it to file
    :param data: data to generate (str)
    :param filename: path to save the qr code (str)
    :return: None
    """
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")
    img.save(filename)

