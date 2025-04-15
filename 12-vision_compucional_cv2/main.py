import cv2 # Librería OpenCv para el procesamiento de imágenes y videos 

## Modelo preentrenados de OpenCv
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') # Detectar Rosotros 
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml') # Detectar Sonrisas 

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read() #Frame = contiene cada fotograma 
    if not ret:
        break

    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar caras
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)  

    for (x, y, w, h) in faces:
        # Dibujar rectángulo alrededor de la cara
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detectar sonrisas dentro de la cara
        smiles = smile_cascade.detectMultiScale(roi_gray, scaleFactor=1.8, minNeighbors=20)

        if len(smiles) > 0:
            mensaje = "Esta feliz, un guapeton"
            color = (0, 255, 0)
        else:
            mensaje = "Triste o enojado"
            color = (0, 0, 255)

        # Mostrar el mensaje
        cv2.putText(frame, mensaje, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Mostrar resultado
    cv2.imshow("Deteccion de sonrisa", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
