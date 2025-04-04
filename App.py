{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyO0ZXpmpvoFtQ4Dq+CGb9G7"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "# pip install streamlit lasio pandas numpy scikit-learn xgboost matplotlib"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "gMdgQr2XPG6K",
        "outputId": "36728e9d-549b-4ecf-c08f-89e9dd6d0dae"
      },
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: streamlit in /usr/local/lib/python3.11/dist-packages (1.44.0)\n",
            "Collecting lasio\n",
            "  Downloading lasio-0.31-py2.py3-none-any.whl.metadata (9.8 kB)\n",
            "Requirement already satisfied: pandas in /usr/local/lib/python3.11/dist-packages (2.2.2)\n",
            "Requirement already satisfied: numpy in /usr/local/lib/python3.11/dist-packages (2.0.2)\n",
            "Requirement already satisfied: scikit-learn in /usr/local/lib/python3.11/dist-packages (1.6.1)\n",
            "Requirement already satisfied: xgboost in /usr/local/lib/python3.11/dist-packages (2.1.4)\n",
            "Requirement already satisfied: matplotlib in /usr/local/lib/python3.11/dist-packages (3.10.0)\n",
            "Requirement already satisfied: altair<6,>=4.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (5.5.0)\n",
            "Requirement already satisfied: blinker<2,>=1.0.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (1.9.0)\n",
            "Requirement already satisfied: cachetools<6,>=4.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (5.5.2)\n",
            "Requirement already satisfied: click<9,>=7.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (8.1.8)\n",
            "Requirement already satisfied: packaging<25,>=20 in /usr/local/lib/python3.11/dist-packages (from streamlit) (24.2)\n",
            "Requirement already satisfied: pillow<12,>=7.1.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (11.1.0)\n",
            "Requirement already satisfied: protobuf<6,>=3.20 in /usr/local/lib/python3.11/dist-packages (from streamlit) (5.29.4)\n",
            "Requirement already satisfied: pyarrow>=7.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (18.1.0)\n",
            "Requirement already satisfied: requests<3,>=2.27 in /usr/local/lib/python3.11/dist-packages (from streamlit) (2.32.3)\n",
            "Requirement already satisfied: tenacity<10,>=8.1.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (9.0.0)\n",
            "Requirement already satisfied: toml<2,>=0.10.1 in /usr/local/lib/python3.11/dist-packages (from streamlit) (0.10.2)\n",
            "Requirement already satisfied: typing-extensions<5,>=4.4.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (4.12.2)\n",
            "Requirement already satisfied: watchdog<7,>=2.1.5 in /usr/local/lib/python3.11/dist-packages (from streamlit) (6.0.0)\n",
            "Requirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /usr/local/lib/python3.11/dist-packages (from streamlit) (3.1.44)\n",
            "Requirement already satisfied: pydeck<1,>=0.8.0b4 in /usr/local/lib/python3.11/dist-packages (from streamlit) (0.9.1)\n",
            "Requirement already satisfied: tornado<7,>=6.0.3 in /usr/local/lib/python3.11/dist-packages (from streamlit) (6.4.2)\n",
            "Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.11/dist-packages (from pandas) (2.8.2)\n",
            "Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.11/dist-packages (from pandas) (2025.1)\n",
            "Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.11/dist-packages (from pandas) (2025.1)\n",
            "Requirement already satisfied: scipy>=1.6.0 in /usr/local/lib/python3.11/dist-packages (from scikit-learn) (1.14.1)\n",
            "Requirement already satisfied: joblib>=1.2.0 in /usr/local/lib/python3.11/dist-packages (from scikit-learn) (1.4.2)\n",
            "Requirement already satisfied: threadpoolctl>=3.1.0 in /usr/local/lib/python3.11/dist-packages (from scikit-learn) (3.6.0)\n",
            "Requirement already satisfied: nvidia-nccl-cu12 in /usr/local/lib/python3.11/dist-packages (from xgboost) (2.21.5)\n",
            "Requirement already satisfied: contourpy>=1.0.1 in /usr/local/lib/python3.11/dist-packages (from matplotlib) (1.3.1)\n",
            "Requirement already satisfied: cycler>=0.10 in /usr/local/lib/python3.11/dist-packages (from matplotlib) (0.12.1)\n",
            "Requirement already satisfied: fonttools>=4.22.0 in /usr/local/lib/python3.11/dist-packages (from matplotlib) (4.56.0)\n",
            "Requirement already satisfied: kiwisolver>=1.3.1 in /usr/local/lib/python3.11/dist-packages (from matplotlib) (1.4.8)\n",
            "Requirement already satisfied: pyparsing>=2.3.1 in /usr/local/lib/python3.11/dist-packages (from matplotlib) (3.2.1)\n",
            "Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from altair<6,>=4.0->streamlit) (3.1.6)\n",
            "Requirement already satisfied: jsonschema>=3.0 in /usr/local/lib/python3.11/dist-packages (from altair<6,>=4.0->streamlit) (4.23.0)\n",
            "Requirement already satisfied: narwhals>=1.14.2 in /usr/local/lib/python3.11/dist-packages (from altair<6,>=4.0->streamlit) (1.31.0)\n",
            "Requirement already satisfied: gitdb<5,>=4.0.1 in /usr/local/lib/python3.11/dist-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.11/dist-packages (from python-dateutil>=2.8.2->pandas) (1.17.0)\n",
            "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (3.4.1)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (3.10)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (2.3.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (2025.1.31)\n",
            "Requirement already satisfied: smmap<6,>=3.0.1 in /usr/local/lib/python3.11/dist-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.2)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->altair<6,>=4.0->streamlit) (3.0.2)\n",
            "Requirement already satisfied: attrs>=22.2.0 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (25.3.0)\n",
            "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (2024.10.1)\n",
            "Requirement already satisfied: referencing>=0.28.4 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.36.2)\n",
            "Requirement already satisfied: rpds-py>=0.7.1 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair<6,>=4.0->streamlit) (0.23.1)\n",
            "Downloading lasio-0.31-py2.py3-none-any.whl (47 kB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m47.4/47.4 kB\u001b[0m \u001b[31m3.6 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hInstalling collected packages: lasio\n",
            "Successfully installed lasio-0.31\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import joblib\n",
        "from xgboost import XGBClassifier # or XGBRegressor, depending on your task\n",
        "\n",
        "model = joblib.load('model.pkl')\n",
        "\n",
        "joblib.dump(model, 'model.pkl')"
      ],
      "metadata": {
        "id": "C3-VO5CaQlaN"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "execution_count": 8,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "5gtWSuejOeIx",
        "outputId": "d702f045-0b0b-447b-d324-c9c41649323c"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "2025-03-31 08:20:09.763 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-31 08:20:09.764 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-31 08:20:09.767 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-31 08:20:09.768 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-31 08:20:09.769 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-31 08:20:09.770 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-31 08:20:09.770 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-31 08:20:09.771 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-31 08:20:09.772 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-31 08:20:09.775 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-03-31 08:20:09.776 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
          ]
        }
      ],
      "source": [
        "import streamlit as st\n",
        "import lasio\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "from sklearn.impute import SimpleImputer\n",
        "from sklearn.preprocessing import MinMaxScaler\n",
        "import joblib\n",
        "import matplotlib.pyplot as plt\n",
        "from io import StringIO, BytesIO\n",
        "\n",
        "# Set page title\n",
        "st.title(\"Kansas Basin Well Log Analyzer\")\n",
        "st.markdown(\"Upload an LAS file to preprocess, predict lithology labels, and visualize the results.\")\n",
        "\n",
        "# Define features and lithology mapping\n",
        "FEATURES = ['GR', 'RHOB', 'RILD', 'DT', 'SP']\n",
        "LITHOLOGY_MAPPING = {0: 'Shale', 1: 'Dolomite', 2: 'Limestone', 3: 'Sandstone', 4: 'Siltstone'}\n",
        "\n",
        "# File uploader for LAS file\n",
        "uploaded_file = st.file_uploader(\"Upload an LAS file\", type=['las'])\n",
        "\n",
        "if uploaded_file is not None:\n",
        "    # Read the LAS file\n",
        "    st.subheader(\"Step 1: Reading the LAS File\")\n",
        "    # Wrap the uploaded file in BytesIO to ensure binary mode\n",
        "    file_content = uploaded_file.read()  # Read the file content as bytes\n",
        "    las = lasio.read(BytesIO(file_content))  # Pass the binary content to lasio\n",
        "    df = las.df().reset_index()  # Convert LAS to DataFrame\n",
        "    st.write(\"Original Data Preview:\")\n",
        "    st.dataframe(df.head())\n",
        "\n",
        "    # Check if required features are present\n",
        "    missing_features = [f for f in FEATURES if f not in df.columns]\n",
        "    if missing_features:\n",
        "        st.error(f\"Missing required features in LAS file: {missing_features}\")\n",
        "    else:\n",
        "        # Preprocessing\n",
        "        st.subheader(\"Step 2: Preprocessing the Data\")\n",
        "\n",
        "        # Handle missing values\n",
        "        st.write(\"Handling missing values using median imputation...\")\n",
        "        imputer = SimpleImputer(strategy='median')\n",
        "        df[FEATURES] = imputer.fit_transform(df[FEATURES])\n",
        "\n",
        "        # Cap outliers in RILD at the 99th percentile\n",
        "        st.write(\"Capping RILD outliers at the 99th percentile...\")\n",
        "        rild_99th = np.percentile(df['RILD'], 99)\n",
        "        df['RILD'] = np.where(df['RILD'] > rild_99th, rild_99th, df['RILD'])\n",
        "\n",
        "        # Scale features to [0, 1]\n",
        "        st.write(\"Scaling features to [0, 1] range...\")\n",
        "        scaler = MinMaxScaler()\n",
        "        df[FEATURES] = scaler.fit_transform(df[FEATURES])\n",
        "\n",
        "        st.write(\"Preprocessed Data Preview:\")\n",
        "        st.dataframe(df.head())\n",
        "\n",
        "        # Predict lithology labels\n",
        "        st.subheader(\"Step 3: Predicting Lithology Labels\")\n",
        "        try:\n",
        "            model = joblib.load('xgboost_model.pkl')\n",
        "            st.write(\"Loaded pre-trained XGBoost model.\")\n",
        "        except FileNotFoundError:\n",
        "            st.error(\"Pre-trained model 'xgboost_model.pkl' not found. Please ensure the model file is in the same directory as this script.\")\n",
        "            st.stop()\n",
        "\n",
        "        # Make predictions\n",
        "        X = df[FEATURES]\n",
        "        predictions = model.predict(X)\n",
        "        df['LITHOLOGY'] = [LITHOLOGY_MAPPING[pred] for pred in predictions]\n",
        "        st.write(\"Data with Predicted Lithology Labels:\")\n",
        "        st.dataframe(df.head())\n",
        "\n",
        "        # Create new LAS file with predictions\n",
        "        st.subheader(\"Step 4: Generating Output LAS File\")\n",
        "        las_out = lasio.LASFile()\n",
        "\n",
        "        # Copy metadata from original LAS file\n",
        "        las_out.well = las.well\n",
        "        las_out.curves = las.curves\n",
        "        las_out.params = las.params\n",
        "        las_out.other = las.other\n",
        "\n",
        "        # Add depth and features to the new LAS file\n",
        "        las_out.append_curve('DEPT', df['DEPT'], unit='FT', descr='Depth')\n",
        "        for feature in FEATURES:\n",
        "            las_out.append_curve(feature, df[feature], unit=las.curves[feature].unit, descr=las.curves[feature].descr)\n",
        "\n",
        "        # Add predicted lithology as a new curve\n",
        "        las_out.append_curve('LITHOLOGY', predictions, unit='', descr='Predicted Lithology (0=Shale, 1=Dolomite, 2=Limestone, 3=Sandstone, 4=Siltstone)')\n",
        "\n",
        "        # Convert LAS to string for download\n",
        "        las_string = StringIO()\n",
        "        las_out.write(las_string)\n",
        "        las_string.seek(0)\n",
        "\n",
        "        # Provide download button for the new LAS file\n",
        "        st.download_button(\n",
        "            label=\"Download LAS File with Lithology Labels\",\n",
        "            data=las_string.getvalue(),\n",
        "            file_name=\"output_with_lithology.las\",\n",
        "            mime=\"text/plain\"\n",
        "        )\n",
        "\n",
        "        # Plotting\n",
        "        st.subheader(\"Step 5: Visualizing Well Logs and Lithology\")\n",
        "        fig, axes = plt.subplots(nrows=1, ncols=len(FEATURES) + 1, figsize=(15, 10), sharey=True)\n",
        "\n",
        "        # Plot each feature\n",
        "        for i, feature in enumerate(FEATURES):\n",
        "            axes[i].plot(df[feature], df['DEPT'], label=feature)\n",
        "            axes[i].set_title(feature)\n",
        "            axes[i].invert_yaxis()\n",
        "            axes[i].grid(True)\n",
        "            if i == 0:\n",
        "                axes[i].set_ylabel('Depth (ft)')\n",
        "\n",
        "        # Plot lithology\n",
        "        lith_colors = {'Shale': 'gray', 'Dolomite': 'blue', 'Limestone': 'green', 'Sandstone': 'yellow', 'Siltstone': 'red'}\n",
        "        lith_numeric = df['LITHOLOGY'].map({v: k for k, v in LITHOLOGY_MAPPING.items()})\n",
        "        axes[-1].scatter(lith_numeric, df['DEPT'], c=df['LITHOLOGY'].map(lith_colors), label='Lithology')\n",
        "        axes[-1].set_title('Lithology')\n",
        "        axes[-1].set_xticks(range(len(LITHOLOGY_MAPPING)))\n",
        "        axes[-1].set_xticklabels(LITHOLOGY_MAPPING.values(), rotation=45)\n",
        "        axes[-1].invert_yaxis()\n",
        "        axes[-1].grid(True)\n",
        "\n",
        "        plt.tight_layout()\n",
        "        st.pyplot(fig)\n",
        "\n",
        "else:\n",
        "    st.info(\"Please upload an LAS file to begin.\")"
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "bVh8IxI2RBhL"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}