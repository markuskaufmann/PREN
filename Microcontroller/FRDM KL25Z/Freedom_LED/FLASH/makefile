################################################################################
# Automatically-generated file. Do not edit!
################################################################################

#Progress monitor hint: 18
first : all
-include ../makefile.init

# This file contains definitions of environment variables used in the makefiles and .args files if exist.
-include makefile.local

RM := "$(GNU_Make_Install_DirEnv)/rm" -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include subdir.mk
-include Sources/subdir.mk
-include Project_Settings/Startup_Code/subdir.mk
-include Generated_Code/subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
ifneq ($(strip $(ASM_DEPS)),)
-include $(ASM_DEPS)
endif
ifneq ($(strip $(ASM_UPPER_DEPS)),)
-include $(ASM_UPPER_DEPS)
endif
ifneq ($(strip $(SX_DEPS)),)
-include $(SX_DEPS)
endif
ifneq ($(strip $(S_DEPS)),)
-include $(S_DEPS)
endif
ifneq ($(strip $(S_UPPER_DEPS)),)
-include $(S_UPPER_DEPS)
endif
endif

-include ../makefile.defs

# Add inputs and outputs from these tool invocations to the build variables 
EXECUTABLES += \
Freedom_LED.elf \

EXECUTABLES_QUOTED += \
"Freedom_LED.elf" \

EXECUTABLES_OS_FORMAT += \
Freedom_LED.elf \

SECONDARY_FLASH += \
Freedom_LED.hex \

SECONDARY_FLASH_QUOTED += \
"Freedom_LED.hex" \

SECONDARY_FLASH_OS_FORMAT += \
Freedom_LED.hex \

SECONDARY_SIZE += \
Freedom_LED.siz \

SECONDARY_SIZE_QUOTED += \
"Freedom_LED.siz" \

SECONDARY_SIZE_OS_FORMAT += \
Freedom_LED.siz \


# All Target
all: warning-messages explicit-dependencies Freedom_LED.elf secondary-outputs

# Tool invocations
Freedom_LED.elf: $(OBJS) $(USER_OBJS) ../Project_Settings/Linker_Files/ProcessorExpert.ld
	@echo 'Building target: $@'
	@echo 'Executing target #19 $@'
	@echo 'Invoking: ARM Ltd Windows GCC C Linker'
	"$(ARMSourceryDirEnv)/arm-none-eabi-gcc"  $(USER_OBJS_QUOTED) $(LIBS_QUOTED) @"Freedom_LED.args" -o"Freedom_LED.elf"
	@echo 'Finished building target: $@'
	@echo ' '

Freedom_LED.hex: Freedom_LED.elf
	@echo 'Executing target #20 $@'
	@echo 'Invoking: ARM Ltd Windows GNU Create Flash Image'
	"$(ARMSourceryDirEnv)/arm-none-eabi-objcopy"  -O srec Freedom_LED.elf  "Freedom_LED.hex"
	@echo 'Finished building: $@'
	@echo ' '

Freedom_LED.siz: Freedom_LED.elf
	@echo 'Executing target #21 $@'
	@echo 'Invoking: ARM Ltd Windows GNU Print Size'
	"$(ARMSourceryDirEnv)/arm-none-eabi-size"  --format=berkeley Freedom_LED.elf
	@echo 'Finished building: $@'
	@echo ' '

# Other Targets
clean:
	-$(RM) $(S_DEPS_QUOTED) $(SECONDARY_FLASH_QUOTED) "./*/*.o" "./*/*/*.o"  $(S_UPPER_DEPS_QUOTED) $(ASM_DEPS_QUOTED) $(SECONDARY_SIZE_QUOTED) $(ASM_UPPER_DEPS_QUOTED) $(SX_DEPS_QUOTED) $(EXECUTABLES_QUOTED) "./*/*.d" "./*/*/*.d"  $(ProjDirPath)/FLASH/Freedom_LED.elf
	-@echo ' '

secondary-outputs: $(SECONDARY_FLASH) $(SECONDARY_SIZE)

.PHONY: all clean dependents explicit-dependencies warning-messages
.SECONDARY:

-include ../makefile.targets

explicit-dependencies: ../Project_Settings/Linker_Files/ProcessorExpert.ld Freedom_LED.elf Freedom_LED.elf 

warning-messages: 

