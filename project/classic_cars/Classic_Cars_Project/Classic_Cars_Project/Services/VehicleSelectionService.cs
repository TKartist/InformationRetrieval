using System;
namespace Classic_Cars_Project.Services

{
    public class VehicleSelectionService
    {
        public Vehicle SelectedVehicle { get; private set; }

        public event Action OnVehicleSelected;

        public void SelectVehicle(Vehicle vehicle)
        {
            SelectedVehicle = vehicle;
            OnVehicleSelected?.Invoke();
        }
    }

}

