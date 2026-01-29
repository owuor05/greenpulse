import React, { useState, useMemo, useCallback } from 'react';
import { MapContainer, GeoJSON, useMap } from 'react-leaflet';
import L from 'leaflet';
import kenyanCountiesData from '../data/kenyan-counties.json';

// Fix Leaflet default icon issue with Webpack
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Component to auto-fit map bounds to Kenya
const FitBounds = () => {
  const map = useMap();
  React.useEffect(() => {
    // Kenya bounds: approximate center and zoom
    map.setView([-0.0236, 37.9062], 6);
  }, [map]);
  return null;
};

const KenyaRiskMap = ({ onCountyClick, degradedCounties = [] }) => {
  const [hoveredCounty, setHoveredCounty] = useState(null);
  const [selectedCounty, setSelectedCounty] = useState(null);

  // County data with severity levels - normalize county names to match GeoJSON
  const countyData = useMemo(() => ({
    'SAMBURU': { severity: 'critical' },
    'KITUI': { severity: 'critical' },
    'GARISSA': { severity: 'critical' },
    'TANA RIVER': { severity: 'critical' },
    'MANDERA': { severity: 'critical' },
    'TURKANA': { severity: 'critical' },
    'MARSABIT': { severity: 'critical' },
    'BARINGO': { severity: 'high' },
    'KAJIADO': { severity: 'high' },
    'KILIFI': { severity: 'high' },
    'WAJIR': { severity: 'high' },
    'MAKUENI': { severity: 'high' },
    'ELGEYO MARAKWET': { severity: 'high' }
  }), []);

  // Severity colors
  const severityColors = useMemo(() => ({
    critical: '#DC2626',
    high: '#F59E0B',
    moderate: '#FBBF24',
    low: '#10B981',
    default: '#E5E7EB'
  }), []);

  const getSeverityColor = useCallback((countyName) => {
    const normalizedName = countyName?.toUpperCase();
    const severity = countyData[normalizedName]?.severity;
    return severityColors[severity] || severityColors.default;
  }, [countyData, severityColors]);

  const handleCountyClick = useCallback((countyName) => {
    setSelectedCounty(countyName);
    const normalizedName = countyName?.toUpperCase();
    if (onCountyClick && countyData[normalizedName]) {
      onCountyClick(countyName, countyData[normalizedName]);
    }
  }, [onCountyClick, countyData]);

  // Style function for GeoJSON features
  const styleFeature = useCallback((feature) => {
    const countyName = feature.properties.COUNTY_NAM;
    const normalizedName = countyName?.toUpperCase();
    const isMonitored = countyData[normalizedName];
    const isHovered = hoveredCounty === countyName;
    const isSelected = selectedCounty === countyName;

    return {
      fillColor: getSeverityColor(countyName),
      weight: isSelected ? 3 : isHovered ? 2 : 1,
      opacity: 1,
      color: isSelected ? '#000000' : '#ffffff',
      fillOpacity: isMonitored ? (isHovered ? 0.9 : 0.7) : 0.3
    };
  }, [getSeverityColor, hoveredCounty, selectedCounty, countyData]);

  // Event handlers for each feature
  const onEachFeature = useCallback((feature, layer) => {
    const countyName = feature.properties.COUNTY_NAM;
    const normalizedName = countyName?.toUpperCase();
    const countyInfo = countyData[normalizedName];

    layer.on({
      mouseover: () => {
        setHoveredCounty(countyName);
        layer.setStyle({
          weight: 2,
          fillOpacity: 0.9
        });
      },
      mouseout: () => {
        setHoveredCounty(null);
      },
      click: () => {
        if (countyInfo) {
          handleCountyClick(countyName);
        }
      }
    });

    // Add tooltip for monitored counties
    if (countyInfo) {
      layer.bindTooltip(
        `<div class="font-semibold">${countyName}</div>
         <div class="text-xs">Risk: <span class="capitalize">${countyInfo.severity}</span></div>`,
        {
          permanent: false,
          direction: 'top',
          className: 'bg-black bg-opacity-75 text-white px-2 py-1 rounded text-sm'
        }
      );
    }
  }, [countyData, handleCountyClick]);

  return (
    <div className="w-full">
      {/* Legend */}
      <div className="mb-4 p-4 bg-white rounded-lg shadow-sm">
        <h3 className="text-lg font-bold text-gray-800 mb-3">Kenya Land Degradation Risk Map</h3>
        <div className="flex flex-wrap gap-4 mb-2">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-red-600"></div>
            <span className="text-sm text-gray-700">Critical Risk (7 counties)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-amber-500"></div>
            <span className="text-sm text-gray-700">High Risk (6 counties)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-gray-300"></div>
            <span className="text-sm text-gray-700">Other counties</span>
          </div>
        </div>
        <p className="text-xs text-gray-600">
          Click any highlighted county to view details and analyze current land data
        </p>
      </div>

      {/* Leaflet Map Container */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div style={{ height: '600px', width: '100%' }}>
          <MapContainer
            center={[-0.0236, 37.9062]}
            zoom={6.5}
            style={{ height: '100%', width: '100%', backgroundColor: '#ffffff' }}
            scrollWheelZoom={false}
            zoomControl={false}
            dragging={false}
            doubleClickZoom={false}
            attributionControl={false}
          >
            <GeoJSON
              data={kenyanCountiesData}
              style={styleFeature}
              onEachFeature={onEachFeature}
            />
            <FitBounds />
          </MapContainer>
        </div>

        {/* County details panel */}
        {selectedCounty && countyData[selectedCounty?.toUpperCase()] && (
          <div className="p-4 bg-gray-50 border-t">
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-lg font-bold text-gray-800">{selectedCounty}</h4>
              <button
                onClick={() => setSelectedCounty(null)}
                className="text-gray-500 hover:text-gray-700 text-xl font-bold"
              >
                ×
              </button>
            </div>
            
            <div className="mb-3">
              <span 
                className="inline-block px-3 py-1 rounded-full text-xs font-semibold text-white"
                style={{ backgroundColor: getSeverityColor(selectedCounty) }}
              >
                {countyData[selectedCounty?.toUpperCase()].severity.toUpperCase()} RISK
              </span>
            </div>
            
            <p className="text-sm text-gray-600 mb-4">
              This county has been identified as having {countyData[selectedCounty?.toUpperCase()].severity} land degradation risk based on satellite data and climate analysis.
            </p>
            
            <button
              onClick={() => handleCountyClick(selectedCounty)}
              className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors"
            >
              Analyze Detailed Data
            </button>
          </div>
        )}
      </div>

      {/* Statistics */}
      <div className="mt-4 grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-red-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-red-600">7</div>
          <div className="text-sm text-red-700">Critical Risk Counties</div>
        </div>
        <div className="bg-amber-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-amber-600">6</div>
          <div className="text-sm text-amber-700">High Risk Counties</div>
        </div>
        <div className="bg-green-50 p-4 rounded-lg">
          <div className="text-2xl font-bold text-green-600">13</div>
          <div className="text-sm text-green-700">Total Monitored Counties</div>
        </div>
      </div>
    </div>
  );
};

export default KenyaRiskMap;
