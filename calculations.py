"""
CE-LIMS Automated Calculations Module
ASTM standard calculations for various test methods
"""

import math
from typing import Dict, Any

def calculate_penetration_test(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    ASTM D5 - Penetration Test for Bituminous Materials
    
    Args:
        data: Dictionary containing:
            - temperature: Test temperature (°C)
            - needle_load: Needle load (g)
            - readings: List of penetration readings (0.1mm)
    
    Returns:
        Dictionary with calculated results
    """
    readings = data.get('readings', [])
    
    if not readings or len(readings) < 3:
        return {'error': 'At least 3 readings required'}
    
    # Calculate average
    avg_penetration = sum(readings) / len(readings)
    
    # Calculate standard deviation
    variance = sum((x - avg_penetration) ** 2 for x in readings) / len(readings)
    std_dev = math.sqrt(variance)
    
    # Calculate coefficient of variation
    cv = (std_dev / avg_penetration * 100) if avg_penetration > 0 else 0
    
    # Grade classification (typical for asphalt binders)
    if avg_penetration >= 200:
        grade = "40/50"
    elif avg_penetration >= 150:
        grade = "60/70"
    elif avg_penetration >= 100:
        grade = "80/100"
    elif avg_penetration >= 50:
        grade = "85/100"
    else:
        grade = "Unknown"
    
    return {
        'average_penetration': round(avg_penetration, 1),
        'unit': '0.1mm',
        'std_deviation': round(std_dev, 2),
        'coefficient_of_variation': round(cv, 2),
        'grade': grade,
        'pass_fail': 'pass' if cv <= 10 else 'fail',  # Typical acceptance: CV <= 10%
        'formula': 'Average = Σ(readings) / n',
        'standard': 'ASTM D5'
    }

def calculate_compressive_strength(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    ASTM C39 - Compressive Strength of Cylindrical Concrete Specimens
    
    Args:
        data: Dictionary containing:
            - diameter: Specimen diameter (mm)
            - height: Specimen height (mm)
            - max_load: Maximum applied load (kN)
            - age: Age of specimen (days) - optional
    
    Returns:
        Dictionary with calculated results
    """
    diameter = data.get('diameter', 0)
    max_load = data.get('max_load', 0)
    age = data.get('age', 28)
    
    if diameter <= 0 or max_load <= 0:
        return {'error': 'Invalid input values'}
    
    # Calculate cross-sectional area (mm²)
    radius = diameter / 2
    area = math.pi * radius ** 2
    
    # Calculate compressive strength (MPa)
    # Load in kN, Area in mm² → Strength in MPa
    strength = (max_load * 1000) / area
    
    # Typical concrete strength requirements
    if age == 7:
        min_strength = 20  # MPa (typical for 7 days)
    elif age == 28:
        min_strength = 30  # MPa (typical for 28 days)
    else:
        min_strength = 25  # MPa (default)
    
    pass_fail = 'pass' if strength >= min_strength else 'fail'
    
    return {
        'compressive_strength': round(strength, 2),
        'unit': 'MPa',
        'cross_sectional_area': round(area, 2),
        'area_unit': 'mm²',
        'age': age,
        'min_required_strength': min_strength,
        'pass_fail': pass_fail,
        'formula': 'Strength (MPa) = Load (kN) × 1000 / Area (mm²)',
        'standard': 'ASTM C39'
    }

def calculate_proctor_test(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    ASTM D1557 - Modified Proctor Test
    
    Args:
        data: Dictionary containing:
            - mold_volume: Volume of mold (cm³)
            - wet_mass: Mass of wet soil + mold (g)
            - mold_mass: Mass of empty mold (g)
            - water_content: Water content (%)
    
    Returns:
        Dictionary with calculated results
    """
    mold_volume = data.get('mold_volume', 0)
    wet_mass = data.get('wet_mass', 0)
    mold_mass = data.get('mold_mass', 0)
    water_content = data.get('water_content', 0)
    
    if mold_volume <= 0 or wet_mass <= mold_mass:
        return {'error': 'Invalid input values'}
    
    # Calculate wet density
    wet_soil_mass = wet_mass - mold_mass
    wet_density = wet_soil_mass / mold_volume
    
    # Calculate dry density
    dry_density = wet_density / (1 + water_content / 100)
    
    return {
        'wet_density': round(wet_density, 3),
        'dry_density': round(dry_density, 3),
        'unit': 'g/cm³',
        'water_content': water_content,
        'optimum_moisture_content': 'To be determined from curve',
        'maximum_dry_density': 'To be determined from curve',
        'formula': 'Dry Density = Wet Density / (1 + w/100)',
        'standard': 'ASTM D1557'
    }

def calculate_unconfined_compression(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    ASTM D2166 - Unconfined Compressive Strength of Cohesive Soil
    
    Args:
        data: Dictionary containing:
            - diameter: Specimen diameter (mm)
            - height: Initial height (mm)
            - max_load: Maximum load at failure (kN)
            - deformation: Deformation at failure (mm)
    
    Returns:
        Dictionary with calculated results
    """
    diameter = data.get('diameter', 0)
    height = data.get('height', 0)
    max_load = data.get('max_load', 0)
    deformation = data.get('deformation', 0)
    
    if diameter <= 0 or height <= 0 or max_load <= 0:
        return {'error': 'Invalid input values'}
    
    # Calculate initial area
    initial_area = math.pi * (diameter / 2) ** 2
    
    # Calculate strain
    strain = (deformation / height) * 100
    
    # Calculate corrected area (accounting for deformation)
    corrected_area = initial_area / (1 - deformation / height)
    
    # Calculate unconfined compressive strength (qu)
    qu = (max_load * 1000) / corrected_area  # kPa
    
    # Soil consistency classification
    if qu < 25:
        consistency = "Very Soft"
    elif qu < 50:
        consistency = "Soft"
    elif qu < 100:
        consistency = "Medium"
    elif qu < 200:
        consistency = "Stiff"
    elif qu < 400:
        consistency = "Very Stiff"
    else:
        consistency = "Hard"
    
    return {
        'unconfined_compressive_strength': round(qu, 2),
        'unit': 'kPa',
        'strain_at_failure': round(strain, 2),
        'strain_unit': '%',
        'consistency': consistency,
        'formula': 'qu = P / A_corrected',
        'standard': 'ASTM D2166'
    }

def calculate_atterberg_limits(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    ASTM D4318 - Liquid Limit, Plastic Limit, and Plasticity Index
    
    Args:
        data: Dictionary containing:
            - liquid_limit: Liquid limit (%)
            - plastic_limit: Plastic limit (%)
    
    Returns:
        Dictionary with calculated results
    """
    liquid_limit = data.get('liquid_limit', 0)
    plastic_limit = data.get('plastic_limit', 0)
    
    if liquid_limit <= 0 or plastic_limit <= 0:
        return {'error': 'Invalid input values'}
    
    # Calculate plasticity index
    plasticity_index = liquid_limit - plastic_limit
    
    # Soil classification based on plasticity
    if plasticity_index < 7:
        classification = "Non-plastic to Low Plasticity"
    elif plasticity_index < 17:
        classification = "Medium Plasticity"
    else:
        classification = "High Plasticity"
    
    # Activity (requires clay fraction)
    clay_fraction = data.get('clay_fraction', 0)
    activity = plasticity_index / clay_fraction if clay_fraction > 0 else None
    
    result = {
        'liquid_limit': liquid_limit,
        'plastic_limit': plastic_limit,
        'plasticity_index': plasticity_index,
        'classification': classification,
        'formula': 'PI = LL - PL',
        'standard': 'ASTM D4318'
    }
    
    if activity:
        result['activity'] = round(activity, 2)
    
    return result

def calculate_cbr(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    ASTM D1883 - California Bearing Ratio (CBR)
    
    Args:
        data: Dictionary containing:
            - load_2_5mm: Load at 2.5mm penetration (kN)
            - load_5mm: Load at 5mm penetration (kN)
    
    Returns:
        Dictionary with calculated results
    """
    load_2_5mm = data.get('load_2_5mm', 0)
    load_5mm = data.get('load_5mm', 0)
    
    if load_2_5mm <= 0 and load_5mm <= 0:
        return {'error': 'Invalid input values'}
    
    # Standard loads for CBR calculation
    standard_load_2_5mm = 13.24  # kN
    standard_load_5mm = 19.96    # kN
    
    # Calculate CBR values
    cbr_2_5mm = (load_2_5mm / standard_load_2_5mm) * 100 if load_2_5mm > 0 else 0
    cbr_5mm = (load_5mm / standard_load_5mm) * 100 if load_5mm > 0 else 0
    
    # CBR is typically the higher of the two values
    cbr = max(cbr_2_5mm, cbr_5mm)
    
    # Subgrade classification
    if cbr < 3:
        subgrade = "Very Poor"
    elif cbr < 7:
        subgrade = "Poor to Fair"
    elif cbr < 20:
        subgrade = "Fair"
    elif cbr < 50:
        subgrade = "Good"
    else:
        subgrade = "Excellent"
    
    return {
        'cbr_2_5mm': round(cbr_2_5mm, 2),
        'cbr_5mm': round(cbr_5mm, 2),
        'cbr_value': round(cbr, 2),
        'unit': '%',
        'subgrade_classification': subgrade,
        'formula': 'CBR = (Test Load / Standard Load) × 100',
        'standard': 'ASTM D1883'
    }

def auto_calculate(test_standard: str, test_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Automatically calculate test results based on test standard
    
    Args:
        test_standard: ASTM standard code (e.g., 'ASTM D5')
        test_data: Dictionary containing test parameters
    
    Returns:
        Dictionary with calculated results
    """
    calculators = {
        'ASTM D5': calculate_penetration_test,
        'ASTM C39': calculate_compressive_strength,
        'ASTM D1557': calculate_proctor_test,
        'ASTM D2166': calculate_unconfined_compression,
        'ASTM D4318': calculate_atterberg_limits,
        'ASTM D1883': calculate_cbr,
    }
    
    calculator = calculators.get(test_standard)
    
    if calculator:
        return calculator(test_data)
    else:
        return {
            'error': f'No calculator available for {test_standard}',
            'manual_entry_required': True
        }

# Example usage and testing
if __name__ == "__main__":
    # Test penetration calculation
    pen_data = {
        'temperature': 25,
        'needle_load': 100,
        'readings': [65, 67, 66]
    }
    print("Penetration Test:", calculate_penetration_test(pen_data))
    
    # Test compressive strength
    comp_data = {
        'diameter': 150,
        'height': 300,
        'max_load': 450,
        'age': 28
    }
    print("\nCompressive Strength:", calculate_compressive_strength(comp_data))
    
    # Test unconfined compression
    uc_data = {
        'diameter': 50,
        'height': 100,
        'max_load': 2.5,
        'deformation': 10
    }
    print("\nUnconfined Compression:", calculate_unconfined_compression(uc_data))
