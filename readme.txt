// size: 12
typedef struct FstorageHeadRegionTag
{
    uint32_t uuid;
    uint8_t model1;
    uint8_t model2; // reserve
    uint16_t ver;
    uint16_t nodeSize;
    uint16_t nodeNum;
} FstorageHeadRegion;

// size: 68
typedef struct _StoreStatisticData
{
    uint8_t mode;
    uint8_t averageHr;
    uint8_t maxHr;
    int8_t timezone;                    // [-11, 12]
    uint16_t distributed[5];
    uint16_t maxCadence;                // unit: per min
    uint32_t riseAtmosphericPressure;   // unit: pa
    uint32_t dropAtmosphericPressure;   // unit: pa
    uint32_t maxAtmosphericPressure;    // unit: pa
    uint32_t minAtmosphericPressure;    // unit: pa
    uint32_t atmosphericPressure;
    uint32_t calorie;
    uint32_t bestPace;                  // unit: sec per kilometer / meter per hour
    uint32_t timestamp;
    uint32_t accomplishTime;            // unit: sec
    uint32_t pauseTime;                 // unit: sec
    uint32_t distance;                  // unit: meter
    uint32_t calibrateDistance;         // unit: meter
    uint32_t step;
} StoreStatisticsData;

// size: 24
typedef struct _StoreRealtimeData
{
    uint8_t pause;
    uint8_t hr; // reserve
    uint8_t longitude_ew;
    uint8_t latitude_ns;
    uint16_t cadence;
    int16_t temperature;
    uint32_t pace;
    uint32_t latitude;
    uint32_t longitude;
    uint32_t atmosphericPressure;
} StoreRealtimeData;

// size: 16
typedef struct _StoreCircleElement
{
    uint32_t pace;
    uint32_t elapseTime;
    uint32_t pauseTime;
    uint32_t unit;
} StoreCircleElement;