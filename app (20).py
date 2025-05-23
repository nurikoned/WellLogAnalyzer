# -*- coding: utf-8 -*-
"""App

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CehlEwPz1nguAsyS1yBoLCC57midBC-l
"""

# pip install streamlit lasio pandas numpy scikit-learn xgboost matplotlib

import joblib
from xgboost import XGBClassifier # or XGBRegressor, depending on your task

model = joblib.load('model.pkl')

joblib.dump(model, 'model.pkl')

import streamlit as st
import lasio
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import matplotlib.pyplot as plt
from io import StringIO, BytesIO, TextIOWrapper

# Define the features the model was trained on
# Update this list to include all 34 features that your model expects
# For now, we'll use the currently defined 8 features and add a mechanism to handle the mismatch
CURRENT_FEATURES = ['GR', 'RHOB', 'RILD', 'DT', 'SP', 'SPOR', 'RILM', 'RLL3']
LITHOLOGY_MAPPING = {0: 'Shale', 1: 'Dolomite', 2: 'Limestone', 3: 'Sandstone', 4: 'Siltstone'}

# Load the pre-trained model
@st.cache_resource
def load_model():
    try:
        model = joblib.load('model.pkl')
        # Get the actual number of features the model was trained on
        if hasattr(model, 'n_features_in_'):
            actual_features = model.n_features_in_
        elif hasattr(model, 'feature_names_in_'):
            actual_features = len(model.feature_names_in_)
        elif hasattr(model, 'get_booster') and hasattr(model.get_booster(), 'num_features'):
            actual_features = model.get_booster().num_features()
        else:
            # Default to the current features if can't determine
            actual_features = len(CURRENT_FEATURES)
        return model, actual_features
    except FileNotFoundError:
        st.error("Model file 'model.pkl' not found. Please ensure the model file is in the same directory as this script.")
        st.stop()

# Streamlit app setup
st.title("Kansas Basin Well Log Analyzer")
st.markdown("Upload an LAS file to preprocess, predict lithology labels, and visualize the results.")

# Load model and get actual feature count
model, actual_feature_count = load_model()
st.info(f"Loaded model expects {actual_feature_count} features. Current configuration uses {len(CURRENT_FEATURES)} features.")

# File uploader for LAS file
uploaded_file = st.file_uploader("Upload an LAS file", type=['las'])

if uploaded_file is not None:
    # Read the LAS file
    st.subheader("Step 1: Reading the LAS File")
    try:
        # Read the file content as bytes and wrap in TextIOWrapper for lasio
        file_content = uploaded_file.read()
        text_stream = TextIOWrapper(BytesIO(file_content), encoding='utf-8')
        las = lasio.read(text_stream)
        df = las.df().reset_index()  # Convert LAS to DataFrame
        st.write("Original Data Preview:")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Error reading LAS file: {e}")
        st.stop()

    # Check if 'DEPTH' column exists and rename to 'DEPT'
    if 'DEPTH' in df.columns:
        st.write("Renaming 'DEPTH' column to 'DEPT' for consistency...")
        df.rename(columns={'DEPTH': 'DEPT'}, inplace=True)
        # Update the LAS object to reflect the renamed column
        for curve in las.curves:
            if curve.mnemonic == 'DEPTH':
                curve.mnemonic = 'DEPT'
                break
    elif 'DEPT' not in df.columns:
        st.error("No 'DEPT' or 'DEPTH' column found in the LAS file. Please ensure the file contains a depth column.")
        st.stop()

    # Feature handling based on model requirements
    st.subheader("Step 2: Feature Analysis")

    # Collect all available log curves from the LAS file
    available_features = [col for col in df.columns if col != 'DEPT']
    st.write(f"Available features in LAS file: {', '.join(available_features)}")

    # Display feature mismatch warning if needed
    if actual_feature_count != len(CURRENT_FEATURES):
        st.warning(f"""
        **Model/Feature Mismatch Detected**

        Your model was trained on {actual_feature_count} features, but your code is configured for {len(CURRENT_FEATURES)} features.

        To resolve this issue, you have two options:
        1. Update the CURRENT_FEATURES list in your code to include all features used during training
        2. Retrain your model using only the {len(CURRENT_FEATURES)} features currently defined

        For now, we'll attempt to adapt the input data, but predictions may not be accurate.
        """)

    # Analysis mode selection
    analysis_mode = st.radio(
        "Select analysis mode:",
        ["Use available features (may be less accurate)", "View available features only (no prediction)"]
    )

    if analysis_mode == "View available features only (no prediction)":
        # Just display the available data
        st.subheader("Available Well Log Data")
        st.dataframe(df)

        # Plot available logs
        st.subheader("Well Log Visualization")
        plot_features = st.multiselect("Select logs to display:", available_features)

        if plot_features:
            fig, axes = plt.subplots(nrows=1, ncols=len(plot_features), figsize=(15, 10), sharey=True)

            # Handle single feature case
            if len(plot_features) == 1:
                axes = [axes]

            # Plot each selected feature
            for i, feature in enumerate(plot_features):
                axes[i].plot(df[feature], df['DEPT'], label=feature)
                axes[i].set_title(feature)
                axes[i].invert_yaxis()
                axes[i].grid(True)
                if i == 0:
                    axes[i].set_ylabel('Depth (ft)')

            plt.tight_layout()
            st.pyplot(fig)

    else:
        # Identify which current features are available in the dataset
        available_current_features = [f for f in CURRENT_FEATURES if f in df.columns]
        missing_features = [f for f in CURRENT_FEATURES if f not in df.columns]

        # Add missing features as NaN columns
        for feature in missing_features:
            df[feature] = np.nan  # Add missing columns with NaN

        if missing_features:
            st.warning(f"Features {missing_features} are missing and were added as NaN. Predictions may be less accurate.")

        # Remove rows where all features are NaN
        st.subheader("Step 3: Filtering Rows with Missing Features")
        st.write("Removing rows where all features are NaN...")
        # Debug: Show the state of feature columns before filtering
        st.write("Feature Columns (Before Filtering):")
        st.dataframe(df[CURRENT_FEATURES].head())

        # Filter out rows where all features are NaN
        df_filtered = df.dropna(subset=CURRENT_FEATURES, how='all')

        # Debug: Show the filtered DataFrame
        st.write("Data After Filtering (Rows with at least one non-NaN feature):")
        st.dataframe(df_filtered.head())

        # Check if the filtered DataFrame is empty
        if df_filtered.empty:
            st.error("After filtering, no rows remain because all features are NaN in all rows. Please upload an LAS file with at least some non-NaN feature data.")
            st.stop()

        # Update df to use the filtered DataFrame
        df = df_filtered

        # Preprocess the data
        st.subheader("Step 4: Preprocessing the Data")

        # Feature engineering based on model requirements
        if actual_feature_count > len(CURRENT_FEATURES):
            st.warning(f"""
            Model expects {actual_feature_count} features but we only have {len(CURRENT_FEATURES)} features defined.
            We will attempt to adapt the input by adding synthetic features to match the model's expectations.
            """)

            # Strategy: Create derived features from existing ones to match the expected count
            # This is a basic approach - ideally you'd know which specific features the model needs
            X_prepared = df[CURRENT_FEATURES].copy()

            # Fill NaNs with mean of each column
            for col in X_prepared.columns:
                X_prepared[col] = X_prepared[col].fillna(X_prepared[col].mean())
                # Replace remaining NaNs (if a column is all NaN) with 0
                X_prepared[col] = X_prepared[col].fillna(0)

            # Scale features to [0, 1] range
            scaler = MinMaxScaler()
            X_scaled = scaler.fit_transform(X_prepared)
            X_prepared = pd.DataFrame(X_scaled, columns=CURRENT_FEATURES)

            # Add synthetic features to match the expected feature count
            features_to_add = actual_feature_count - len(CURRENT_FEATURES)
            synthetic_features = []

            for i in range(features_to_add):
                # Create synthetic features as combinations of existing ones
                if i < len(CURRENT_FEATURES):
                    # Use simple transforms of existing features
                    feature_name = f"SYNTH_{i+1}"
                    X_prepared[feature_name] = X_prepared[CURRENT_FEATURES[i % len(CURRENT_FEATURES)]] ** 2
                    synthetic_features.append(feature_name)
                else:
                    # For any remaining features needed, use random values
                    feature_name = f"SYNTH_{i+1}"
                    X_prepared[feature_name] = np.random.rand(len(X_prepared))
                    synthetic_features.append(feature_name)

            st.write(f"Added {features_to_add} synthetic features to match model requirements.")

            # Now X_prepared has the right number of features for prediction
            X = X_prepared

        else:
            # Standard processing for the current features
            X = df[CURRENT_FEATURES].copy()

            # Fill NaNs with column means
            for col in X.columns:
                X[col] = X[col].fillna(X[col].mean())
                # Replace remaining NaNs (if a column is all NaN) with 0
                X[col] = X[col].fillna(0)

            # Scale features to [0, 1] range
            scaler = MinMaxScaler()
            X_scaled = scaler.fit_transform(X)
            X = pd.DataFrame(X_scaled, columns=CURRENT_FEATURES)

        st.write("Preprocessed Data Preview:")
        st.dataframe(X.head())

        # Predict lithology labels
        st.subheader("Step 5: Predicting Lithology Labels")

        try:
            predictions = model.predict(X)
            df['LITHOLOGY_LABEL'] = [LITHOLOGY_MAPPING.get(int(pred), f"Unknown-{pred}") for pred in predictions]
            st.write("Data with Predicted Lithology Labels:")
            st.dataframe(df[['DEPT'] + CURRENT_FEATURES + ['LITHOLOGY_LABEL']].head())

            # Create new LAS file with numeric predictions
            st.subheader("Step 6: Generating Output LAS File")
            las_out = lasio.LASFile()

            # Copy metadata from original LAS file
            las_out.well = las.well
            las_out.curves = las.curves
            las_out.params = las.params
            las_out.other = las.other

            # Add depth and features to the new LAS file
            las_out.append_curve('DEPT', df['DEPT'], unit='FT', descr='Depth')
            for feature in CURRENT_FEATURES:
                las_out.append_curve(feature, df[feature],
                                    unit=las.curves[feature].unit if feature in las.curves else '',
                                    descr=las.curves[feature].descr if feature in las.curves else '')

            # Add predicted lithology as a numeric curve
            las_out.append_curve('LITHOLOGY', predictions, unit='',
                                descr='Predicted Lithology (0=Shale, 1=Dolomite, 2=Limestone, 3=Sandstone, 4=Siltstone)')

            # Generate downloadable files
            las_string = StringIO()
            las_out.write(las_string)
            las_string.seek(0)

            # Provide download button for the LAS file
            st.download_button(
                label="Download LAS File with Numeric Lithology Codes",
                data=las_string.getvalue(),
                file_name="output_with_lithology.las",
                mime="text/plain"
            )

            # Provide a downloadable CSV with depth and lithology labels
            st.subheader("Step 7: Download Lithology Labels as CSV")
            output_df = df[['DEPT', 'LITHOLOGY_LABEL']]
            csv = output_df.to_csv(index=False)
            st.download_button(
                label="Download Lithology Labels (Depth and Names)",
                data=csv,
                file_name="lithology_labels.csv",
                mime="text/csv"
            )

            # Plotting
            st.subheader("Step 8: Visualizing Well Logs and Lithology")

            # Select features to display
            plot_features = st.multiselect("Select logs to display:", CURRENT_FEATURES,
                                          default=CURRENT_FEATURES[:min(4, len(CURRENT_FEATURES))])

            if plot_features:
                fig, axes = plt.subplots(nrows=1, ncols=len(plot_features) + 1, figsize=(15, 10), sharey=True)

                # Handle single feature case
                if len(plot_features) == 1:
                    axes = [axes[0], axes[1]]

                # Plot each feature
                for i, feature in enumerate(plot_features):
                    axes[i].plot(df[feature], df['DEPT'], label=feature)
                    axes[i].set_title(feature)
                    axes[i].invert_yaxis()
                    axes[i].grid(True)
                    if i == 0:
                        axes[i].set_ylabel('Depth (ft)')

                # Plot lithology
                lith_colors = {'Shale': 'gray', 'Dolomite': 'blue', 'Limestone': 'green', 'Sandstone': 'yellow', 'Siltstone': 'red'}
                lith_idx = len(plot_features)

                # Create a categorical representation for plotting
                lith_numeric = pd.Series([k for k, v in LITHOLOGY_MAPPING.items() for label in df['LITHOLOGY_LABEL']
                                         if v == label]).values

                # Create color list
                colors = [lith_colors.get(label, 'black') for label in df['LITHOLOGY_LABEL']]

                axes[lith_idx].scatter(np.zeros(len(df)), df['DEPT'], c=colors, label='Lithology')
                axes[lith_idx].set_title('Lithology')
                axes[lith_idx].set_xticks([])

                # Create legend
                from matplotlib.patches import Patch
                legend_elements = [Patch(facecolor=color, label=name) for name, color in lith_colors.items()]
                axes[lith_idx].legend(handles=legend_elements, loc='upper right')

                axes[lith_idx].invert_yaxis()
                axes[lith_idx].grid(True)

                plt.tight_layout()
                st.pyplot(fig)

        except Exception as e:
            st.error(f"Error making predictions: {e}")
            st.error("""
            The model cannot make predictions with the current features. This could be due to:
            1. A mismatch between the model's expected features and the provided features
            2. Data format issues
            3. NaN values or other data quality problems

            Please consider retraining your model with the available features or providing a dataset with the required features.
            """)

            # Still show the available data visualization
            st.subheader("Available Well Log Data Visualization")
            plot_features = st.multiselect("Select logs to display:", available_features)

            if plot_features:
                fig, axes = plt.subplots(nrows=1, ncols=len(plot_features), figsize=(15, 10), sharey=True)

                # Handle single feature case
                if len(plot_features) == 1:
                    axes = [axes]

                # Plot each selected feature
                for i, feature in enumerate(plot_features):
                    axes[i].plot(df[feature], df['DEPT'], label=feature)
                    axes[i].set_title(feature)
                    axes[i].invert_yaxis()
                    axes[i].grid(True)
                    if i == 0:
                        axes[i].set_ylabel('Depth (ft)')

                plt.tight_layout()
                st.pyplot(fig)

else:
    st.info("Please upload an LAS file to begin.")

