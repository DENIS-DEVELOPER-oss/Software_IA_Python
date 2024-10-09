from models import modelo_para_prediccion
from dataset import CassavaDataset, get_transforms, classes
from inference import load_state, inference
from utils import CFG
from grad_cam import SaveFeatures, getCAM
import gc
import torch
from torch.utils.data import DataLoader, Dataset
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from html_markdown import ( 
    app_off2,  
    model_predicting, 
    image_uploaded_success, 
    class0,  
    class1,  
    class2,  
    class3,  
    class4,  
    class0_side, 
    class1_side, 
    class2_side, 
    class3_side, 
    class4_side, 
    unknown,  
    unknown_side,
    unknown_w,
    unknown_msg,
)

# Ocultar advertencias
st.set_option("deprecation.showfileUploaderEncoding", False)

# Establecer el título de la aplicación
st.image("imagenes/logo.png", use_column_width=True)

# Establecer la ruta del directorio
my_path = "."

test = pd.read_csv(my_path + "/data/Test.csv")
img_1_path = my_path + "/imagenes/img_1.jpg"
img_2_path = my_path + "/imagenes/img_2.jpg"
img_3_path = my_path + "/imagenes/img_3.jpg"
output_image = my_path + "/imagenes/gradcam2.png"


# Establecer el selectbox para imágenes de demostración
st.write("**Selecciona una imagen para una DEMOSTRACIÓN**")
menu = ["Seleccionar una imagen", "Imagen 1", "Imagen 2", "Imagen 3"]
choice = st.selectbox("Selecciona una imagen", menu)

# Establecer la caja para que el usuario suba una imagen
st.write("**Sube tu imagen**")
uploaded_image = st.file_uploader(
    "Sube tu imagen en formato JPG o PNG", type=["jpg", "png"]
)

# DataLoader para el conjunto de datos pytorch
def Loader(img_path=None, uploaded_image=None, upload_state=False, demo_state=True):
    test_dataset = CassavaDataset(
        test,
        img_path,
        uploaded_image=uploaded_image,
        transform=get_transforms(data="valid"),
        uploaded_state=upload_state,
        demo_state=demo_state,
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=CFG.batch_size,
        shuffle=False,
        num_workers=CFG.num_workers,
        pin_memory=True,
    )
    return test_loader

# Función para desplegar el modelo e imprimir el informe
def deploy(file_path=None, uploaded_image=uploaded_image, uploaded=False, demo=True):
    # Cargar el modelo y los pesos
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = modelo_para_prediccion(CFG.model_name, pretrained=False)
    states = [load_state(my_path + "/modelo/modelo_para_prediccion.pth")]

    # Para características de Grad-cam
    final_conv = model.model.layer4[2]._modules.get("conv3")
    fc_params = list(model.model._modules.get("fc").parameters())

    # Mostrar la imagen subida/seleccionada
    st.markdown("***")
    st.markdown(model_predicting, unsafe_allow_html=True)
    if demo:
        test_loader = Loader(img_path=file_path)
        image_1 = cv2.imread(file_path)
    if uploaded:
        test_loader = Loader(
            uploaded_image=uploaded_image, upload_state=True, demo_state=False
        )
        image_1 = file_path
    st.sidebar.markdown(image_uploaded_success, unsafe_allow_html=True)
    st.sidebar.image(image_1, width=301, channels="BGR")

    for img in test_loader:
        activated_features = SaveFeatures(final_conv)
        # Guardar peso de fc
        weight = np.squeeze(fc_params[0].cpu().data.numpy())

        # Inferencia
        logits, output = inference(model, states, img, device)
        pred_idx = output.to("cpu").numpy().argmax(1)

        # Grad-cam heatmap display
        heatmap = getCAM(activated_features.features, weight, pred_idx)

        ##Revertir la normalización de pytorch
        MEAN = torch.tensor([0.485, 0.456, 0.406])
        STD = torch.tensor([0.229, 0.224, 0.225])
        image = img[0] * STD[:, None, None] + MEAN[:, None, None]

        # Mostrar imagen + heatmap
        plt.imshow(image.permute(1, 2, 0))
        plt.imshow(
            cv2.resize(
                (heatmap * 255).astype("uint8"),
                (328, 328),
                interpolation=cv2.INTER_LINEAR,
            ),
            alpha=0.4,
            cmap="jet",
        )
        plt.savefig(output_image)

        # Mostrar clase desconocida si la probabilidad más alta es inferior a 0.5
        if np.amax(logits) < 0.57:
            st.markdown(unknown, unsafe_allow_html=True)
            st.sidebar.markdown(unknown_side, unsafe_allow_html=True)
            st.sidebar.markdown(unknown_w, unsafe_allow_html=True)
        # Muestra la clase predicha si la probabilidad más alta es superior a 0.5
        else:
            if pred_idx[0] == 0:
                st.markdown(class0, unsafe_allow_html=True)
                st.sidebar.markdown(class0_side, unsafe_allow_html=True)
                st.write(" Prediccion: **Tizón bacteriano**")
            elif pred_idx[0] == 1:
                st.markdown(class1, unsafe_allow_html=True)
                st.sidebar.markdown(class1_side, unsafe_allow_html=True)
                st.write(
                    "Prediccion: **Enfermedad de la raya marrón**"
                )
            elif pred_idx[0] == 2:
                st.markdown(class2, unsafe_allow_html=True)
                st.sidebar.markdown(class2_side, unsafe_allow_html=True)
                st.write("Prediccion: **Mandioca Verde Moteada**")
            elif pred_idx[0] == 3:
                st.markdown(class3, unsafe_allow_html=True)
                st.sidebar.markdown(class3_side, unsafe_allow_html=True)
                st.write("Prediccion: ** Enfermedad del mosaico**")
            elif pred_idx[0] == 4:
                st.markdown(class4, unsafe_allow_html=True)
                st.sidebar.markdown(class4_side, unsafe_allow_html=True)
                st.write("Prediccion: **Saludable**")


        # Mostrar la imagen Grad-Cam
        st.title("**Predicciones  través de Grad-CAM**")
        st.write(
            "* Resalta las regiones importantes en la imagen para predecir el concepto de la clase. Ayuda a entender si el modelo basó sus predicciones en las regiones correctas de la imagen."
        )
        gram_im = cv2.imread(output_image)
        st.image(gram_im, width=528, channels="RGB")

        # Mostrar la tabla de probabilidades de clase
        st.title("**Emfermedades Posibles:**")
        st.write(
            "* En esta seccion se muestra una tabla con las emfermedades posibles y su respectiva probabilidad, la emfermedad con mas probabilidad se mostrara en rojo dentro de la tabla.."
        )
        if np.amax(logits) < 0.57:
            st.markdown(unknown_msg, unsafe_allow_html=True)
        classes["probabilidad  %"] = logits.reshape(-1).tolist()
        classes["probabilidad  %"] = classes["probabilidad  %"] * 100
        clases_proba = classes.style.background_gradient(cmap="Reds")
        st.write(clases_proba)
        del (
            model,
            states,
            fc_params,
            final_conv,
            test_loader,
            image_1,
            activated_features,
            weight,
            heatmap,
            gram_im,
            logits,
            output,
            pred_idx,
            clases_proba,
        )
        gc.collect()

# Establecer bandera roja si no se selecciona/sube ninguna imagen
st.sidebar.markdown("<h1 style='text-align: center; color: black;'>GREEN SPECTRE</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='text-align: justify'>Esta es una aplicación web de diagnóstico de enfermedades en plantas, diseñada para identificar y clasificar diversas enfermedades en una amplia variedad de plantas a partir de imágenes. La aplicación utiliza un avanzado modelo de aprendizaje automático, entrenado previamente con un amplio conjunto de datos de imágenes de plantas, para realizar las predicciones.</div>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border:1px solid Green'>", unsafe_allow_html=True)
st.sidebar.markdown("<h2 style='text-align: justify; font-family:Barlow; font-weight:bold;'>Imagenes que puede ingresar</h2>", unsafe_allow_html=True)


st.sidebar.markdown("- Puede cargar imagenes que contengan hojas de las planta que desea.", unsafe_allow_html=True)
st.sidebar.image("imagenes/hojas.png")

st.sidebar.markdown("- Tambien Puede cargar Imagenes que contengan frutos de la que desea", unsafe_allow_html=True)
st.sidebar.image("imagenes/frutos.jpg")
st.sidebar.markdown("<hr style='border:1px solid Green'>", unsafe_allow_html=True)
if uploaded_image is None and choice == "Seleccionar una imagen":
    st.sidebar.markdown(app_off2, unsafe_allow_html=True)

# Implementar el modelo si el usuario sube una imagen
if uploaded_image is not None:
    # Cerrar la demo
    choice = "Seleccionar una imagen"
    # Implementar el modelo con la imagen subida
    deploy(uploaded_image, uploaded=True, demo=False)
    del uploaded_image

# Implementar el modelo si el usuario selecciona la Imagen 1
if choice == "Imagen 1":
    deploy(img_1_path)

# Implementar el modelo si el usuario selecciona la Imagen 2
if choice == "Imagen 2":
    deploy(img_2_path)

# Implementar el modelo si el usuario selecciona la Imagen 3
if choice == "Imagen 3":
    deploy(img_3_path)
