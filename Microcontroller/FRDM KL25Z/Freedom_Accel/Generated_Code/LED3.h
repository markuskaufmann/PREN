/** ###################################################################
**     THIS COMPONENT MODULE IS GENERATED BY THE TOOL. DO NOT MODIFY IT.
**     Filename    : LED3.h
**     Project     : ProcessorExpert
**     Processor   : MKL25Z128VLK4
**     Component   : LED
**     Version     : Component 01.047, Driver 01.00, CPU db: 3.00.000
**     Compiler    : GNU C Compiler
**     Date/Time   : 2012-12-25, 18:56, # CodeGen: 13
**     Abstract    :
**          This component implements a universal driver for a single LED.
**     Settings    :
**          Component name                                 : LED3
**          LED on with initialization                     : no
**          HW Interface                                   : 
**            LED Pin                                      : LEDpin
**            Anode on port side                           : no
**     Contents    :
**         On     - void LED3_On(void);
**         Off    - void LED3_Off(void);
**         Neg    - void LED3_Neg(void);
**         Get    - byte LED3_Get(void);
**         Put    - void LED3_Put(byte val);
**         Init   - void LED3_Init(void);
**         Deinit - void LED3_Deinit(void);
**
**     License   :  Open Source (LGPL)
**     Copyright : (c) Copyright Erich Styger, 2012, all rights reserved.
**     This an open source software implementing an LED driver using Processor Expert.
**     This is a free software and is opened for education, research and commercial developments under license policy of following terms:
**     * This is a free software and there is NO WARRANTY.
**     * No restriction on use. You can use, modify and redistribute it for personal, non-profit or commercial product UNDER YOUR RESPONSIBILITY.
**     * Redistributions of source code must retain the above copyright notice.
** ###################################################################*/

#ifndef __LED3_H
#define __LED3_H

/* MODULE LED3. */

/* Include shared modules, which are used for whole project */
#include "PE_Types.h"
#include "PE_Error.h"
#include "PE_Const.h"
#include "IO_Map.h"
/* Include inherited beans */
#include "LEDpin6.h"

#include "Cpu.h"

#define LED3_ClrVal()    LEDpin6_ClrVal() /* put the pin on low level */
#define LED3_SetVal()    LEDpin6_SetVal() /* put the pin on high level */
#define LED3_SetInput()  LEDpin6_SetInput() /* use the pin as input pin */
#define LED3_SetOutput() LEDpin6_SetOutput() /* use the pin as ouput pin */


#define LED3_On() LEDpin6_ClrVal()
/*
** ===================================================================
**     Method      :  LED3_On (component LED)
**
**     Description :
**         This turns the LED on.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/

#define LED3_Off() LEDpin6_SetVal()
/*
** ===================================================================
**     Method      :  LED3_Off (component LED)
**
**     Description :
**         This turns the LED off.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/

#define LED3_Neg() LEDpin6_NegVal()
/*
** ===================================================================
**     Method      :  LED3_Neg (component LED)
**
**     Description :
**         This negates/toggles the LED
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/

#define LED3_Get() (!(LEDpin6_GetVal()))
/*
** ===================================================================
**     Method      :  LED3_Get (component LED)
**
**     Description :
**         This returns logical 1 in case the LED is on, 0 otherwise.
**     Parameters  : None
**     Returns     :
**         ---             - Status of the LED (on or off)
** ===================================================================
*/

#define LED3_Init() LED3_Off()
/*
** ===================================================================
**     Method      :  LED3_Init (component LED)
**
**     Description :
**         Performs the LED driver initialization.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/

#define LED3_Put(val)  ((val) ? LED3_On() : LED3_Off())
/*
** ===================================================================
**     Method      :  LED3_Put (component LED)
**
**     Description :
**         Turns the LED on or off.
**     Parameters  :
**         NAME            - DESCRIPTION
**         val             - value to define if the LED has to be on or
**                           off.
**     Returns     : Nothing
** ===================================================================
*/

void LED3_Deinit(void);
/*
** ===================================================================
**     Method      :  LED3_Deinit (component LED)
**
**     Description :
**         Deinitializes the driver
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/

/* END LED3. */

#endif
/* ifndef __LED3_H */
/*
** ###################################################################
**
**     This file was created by Processor Expert 10.0 [05.03]
**     for the Freescale Kinetis series of microcontrollers.
**
** ###################################################################
*/
