export interface Station {
  id: string;
  name: string;
  district: string;
  lat: number;
  lng: number;
  riskFactors: {
    MonsoonIntensity: number;
    TopographyDrainage: number;
    RiverManagement: number;
    Deforestation: number;
    Urbanization: number;
    ClimateChange: number;
    DamsQuality: number;
    Siltation: number;
    AgriculturalPractices: number;
    Encroachments: number;
    IneffectiveDisasterPreparedness: number;
    DrainageSystems: number;
    CoastalVulnerability: number;
    Landslides: number;
    Watersheds: number;
    DeterioratingInfrastructure: number;
    PopulationScore: number;
    WetlandLoss: number;
    InadequatePlanning: number;
    PoliticalFactors: number;
  };
}

export const stations: Station[] = [
  {
    id: "STN001", name: "Uttarkashi", district: "Uttarkashi, Uttarakhand",
    lat: 30.7268, lng: 78.4354,
    riskFactors: {
      MonsoonIntensity: 12, TopographyDrainage: 5, RiverManagement: 6, Deforestation: 10,
      Urbanization: 6, ClimateChange: 11, DamsQuality: 6, Siltation: 9,
      AgriculturalPractices: 7, Encroachments: 6, IneffectiveDisasterPreparedness: 10,
      DrainageSystems: 5, CoastalVulnerability: 2, Landslides: 12, Watersheds: 7,
      DeterioratingInfrastructure: 9, PopulationScore: 6, WetlandLoss: 6,
      InadequatePlanning: 9, PoliticalFactors: 6,
    },
  },
  {
    id: "STN002", name: "Dharali", district: "Uttarkashi, Uttarakhand",
    lat: 31.0408, lng: 78.7811,
    riskFactors: {
      MonsoonIntensity: 15, TopographyDrainage: 4, RiverManagement: 4, Deforestation: 13,
      Urbanization: 4, ClimateChange: 14, DamsQuality: 4, Siltation: 12,
      AgriculturalPractices: 6, Encroachments: 5, IneffectiveDisasterPreparedness: 13,
      DrainageSystems: 4, CoastalVulnerability: 1, Landslides: 16, Watersheds: 8,
      DeterioratingInfrastructure: 12, PopulationScore: 4, WetlandLoss: 7,
      InadequatePlanning: 12, PoliticalFactors: 7,
    },
  },
  {
    id: "STN003", name: "Manali", district: "Kullu, Himachal Pradesh",
    lat: 32.2432, lng: 77.1892,
    riskFactors: {
      MonsoonIntensity: 8, TopographyDrainage: 6, RiverManagement: 6, Deforestation: 7,
      Urbanization: 8, ClimateChange: 7, DamsQuality: 6, Siltation: 6,
      AgriculturalPractices: 6, Encroachments: 7, IneffectiveDisasterPreparedness: 6,
      DrainageSystems: 6, CoastalVulnerability: 2, Landslides: 7, Watersheds: 6,
      DeterioratingInfrastructure: 6, PopulationScore: 8, WetlandLoss: 4,
      InadequatePlanning: 6, PoliticalFactors: 6,
    },
  },
  {
    id: "STN004", name: "Kullu Town", district: "Kullu, Himachal Pradesh",
    lat: 31.9576, lng: 77.1095,
    riskFactors: {
      MonsoonIntensity: 7, TopographyDrainage: 6, RiverManagement: 6, Deforestation: 6,
      Urbanization: 7, ClimateChange: 6, DamsQuality: 6, Siltation: 6,
      AgriculturalPractices: 6, Encroachments: 6, IneffectiveDisasterPreparedness: 6,
      DrainageSystems: 5, CoastalVulnerability: 2, Landslides: 6, Watersheds: 5,
      DeterioratingInfrastructure: 5, PopulationScore: 7, WetlandLoss: 4,
      InadequatePlanning: 5, PoliticalFactors: 5,
    },
  },
  {
    id: "STN005", name: "Rishikesh", district: "Dehradun, Uttarakhand",
    lat: 30.0869, lng: 78.2676,
    riskFactors: {
      MonsoonIntensity: 4, TopographyDrainage: 2, RiverManagement: 2, Deforestation: 2,
      Urbanization: 5, ClimateChange: 3, DamsQuality: 2, Siltation: 2,
      AgriculturalPractices: 4, Encroachments: 3, IneffectiveDisasterPreparedness: 2,
      DrainageSystems: 2, CoastalVulnerability: 1, Landslides: 2, Watersheds: 3,
      DeterioratingInfrastructure: 2, PopulationScore: 5, WetlandLoss: 2,
      InadequatePlanning: 2, PoliticalFactors: 3,
    },
  },
  {
    id: "STN006", name: "Shimla", district: "Shimla, Himachal Pradesh",
    lat: 31.1048, lng: 77.1734,
    riskFactors: {
      MonsoonIntensity: 6, TopographyDrainage: 5, RiverManagement: 5, Deforestation: 4,
      Urbanization: 7, ClimateChange: 5, DamsQuality: 5, Siltation: 4,
      AgriculturalPractices: 5, Encroachments: 6, IneffectiveDisasterPreparedness: 4,
      DrainageSystems: 5, CoastalVulnerability: 2, Landslides: 4, Watersheds: 5,
      DeterioratingInfrastructure: 4, PopulationScore: 7, WetlandLoss: 3,
      InadequatePlanning: 4, PoliticalFactors: 5,
    },
  },
];